"""
erpnext_store.api
~~~~~~~~~~~~~~~~~
All endpoints are called via frappe.call() from the browser.
Guest-accessible methods are decorated with allow_guest=True.
"""

import frappe
from frappe import _


# ──────────────────────────────────────────────────────────────────
# CATALOGUE
# ──────────────────────────────────────────────────────────────────

@frappe.whitelist(allow_guest=True)
def get_store_settings():
    """Return public store configuration."""
    s = frappe.get_single("Store Settings")
    return {
        "store_name": s.store_name,
        "store_tagline": s.store_tagline,
        "currency": s.currency or "USD",
        "require_login_to_order": s.require_login_to_order,
    }


@frappe.whitelist(allow_guest=True)
def get_categories():
    """Return all active store categories."""
    cats = frappe.get_all(
        "Store Category",
        filters={"is_active": 1},
        fields=["name", "category_name", "icon", "description"],
        order_by="sort_order asc, category_name asc",
    )
    return cats


@frappe.whitelist(allow_guest=True)
def get_products(category=None, search=None, page=1, page_size=20):
    """
    Return published Item records.
    Filters by Item Group (mapped to Store Category name) when category is given.
    """
    page = int(page)
    page_size = int(page_size)
    filters = {"disabled": 0, "is_sales_item": 1}

    if category:
        filters["item_group"] = category

    if search:
        filters["item_name"] = ["like", f"%{search}%"]

    items = frappe.get_all(
        "Item",
        filters=filters,
        fields=[
            "name", "item_name", "item_group", "description",
            "image", "standard_rate",
        ],
        limit_start=(page - 1) * page_size,
        limit_page_length=page_size,
        order_by="item_name asc",
    )

    # Pull selling price from price list when available
    settings = frappe.get_single("Store Settings")
    price_list = settings.price_list or "Standard Selling"
    currency = settings.currency or "USD"

    for item in items:
        price_doc = frappe.get_all(
            "Item Price",
            filters={"item_code": item["name"], "price_list": price_list, "selling": 1},
            fields=["price_list_rate", "currency"],
            limit=1,
        )
        if price_doc:
            item["price"] = price_doc[0]["price_list_rate"]
            item["currency"] = price_doc[0]["currency"]
        else:
            item["price"] = item.get("standard_rate") or 0
            item["currency"] = currency

    total = frappe.db.count("Item", filters=filters)
    return {"items": items, "total": total, "page": page, "page_size": page_size}


@frappe.whitelist(allow_guest=True)
def get_product(item_code):
    """Return a single product with full details."""
    item = frappe.get_doc("Item", item_code)
    settings = frappe.get_single("Store Settings")
    price_list = settings.price_list or "Standard Selling"
    currency = settings.currency or "USD"

    price_doc = frappe.get_all(
        "Item Price",
        filters={"item_code": item_code, "price_list": price_list, "selling": 1},
        fields=["price_list_rate", "currency"],
        limit=1,
    )
    price = price_doc[0]["price_list_rate"] if price_doc else (item.standard_rate or 0)
    currency = price_doc[0]["currency"] if price_doc else currency

    return {
        "name": item.name,
        "item_name": item.item_name,
        "item_group": item.item_group,
        "description": item.description,
        "image": item.image,
        "price": price,
        "currency": currency,
        "stock_uom": item.stock_uom,
    }


# ──────────────────────────────────────────────────────────────────
# AUTH / REGISTRATION
# ──────────────────────────────────────────────────────────────────

@frappe.whitelist(allow_guest=True)
def register_and_place_order(
    first_name, last_name, email, phone, password, cart_items
):
    """
    Called when a guest checks out.
    1. Creates a Customer + User if they don't exist.
    2. Logs the user in.
    3. Places a Sales Order.
    Returns the new Sales Order name.
    """
    import json

    cart_items = json.loads(cart_items) if isinstance(cart_items, str) else cart_items

    # ── 1. Create or fetch user ──────────────────────────────────
    if not frappe.db.exists("User", email):
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "send_welcome_email": 0,
            "roles": [{"role": "Customer"}],
        })
        user.new_password = password
        user.insert(ignore_permissions=True)
        frappe.db.commit()
    else:
        user = frappe.get_doc("User", email)

    # ── 2. Create or fetch Customer linked to that user ──────────
    existing_customer = frappe.db.get_value("Customer", {"email_id": email}, "name")
    if existing_customer:
        customer_name = existing_customer
    else:
        customer = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": f"{first_name} {last_name}",
            "customer_type": "Individual",
            "email_id": email,
            "mobile_no": phone,
        })
        customer.insert(ignore_permissions=True)
        customer_name = customer.name
        frappe.db.commit()

    # ── 3. Build and submit Sales Order ─────────────────────────
    settings = frappe.get_single("Store Settings")

    so = frappe.get_doc({
        "doctype": "Sales Order",
        "customer": customer_name,
        "company": settings.company,
        "price_list": settings.price_list or "Standard Selling",
        "currency": settings.currency or "USD",
        "delivery_date": frappe.utils.add_days(frappe.utils.today(), 7),
        "taxes_and_charges": settings.tax_template or "",
        "items": [
            {
                "item_code": row["item_code"],
                "qty": row["qty"],
                "warehouse": settings.warehouse,
            }
            for row in cart_items
        ],
    })
    so.insert(ignore_permissions=True)
    so.submit()
    frappe.db.commit()

    return {"order_name": so.name, "customer": customer_name}


@frappe.whitelist(allow_guest=True)
def login_and_place_order(email, password, cart_items):
    """
    Called when a returning customer checks out.
    Authenticates, then places a Sales Order.
    """
    import json
    from frappe.auth import LoginManager

    cart_items = json.loads(cart_items) if isinstance(cart_items, str) else cart_items

    lm = LoginManager()
    lm.authenticate(email, password)
    lm.post_login()

    customer_name = frappe.db.get_value("Customer", {"email_id": email}, "name")
    if not customer_name:
        frappe.throw(_("No customer account found for {0}").format(email))

    settings = frappe.get_single("Store Settings")

    so = frappe.get_doc({
        "doctype": "Sales Order",
        "customer": customer_name,
        "company": settings.company,
        "price_list": settings.price_list or "Standard Selling",
        "currency": settings.currency or "USD",
        "delivery_date": frappe.utils.add_days(frappe.utils.today(), 7),
        "taxes_and_charges": settings.tax_template or "",
        "items": [
            {
                "item_code": row["item_code"],
                "qty": row["qty"],
                "warehouse": settings.warehouse,
            }
            for row in cart_items
        ],
    })
    so.insert(ignore_permissions=True)
    so.submit()
    frappe.db.commit()

    return {"order_name": so.name, "customer": customer_name}
