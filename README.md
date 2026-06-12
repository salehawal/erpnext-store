# ERPNext Store

A public-facing storefront for ERPNext/Frappe. Accessible at `yoursite.com/store`.

## Features

- Browse products by category (Item Groups mapped to Store Categories)
- Category icons configurable from the admin — random Tabler icon assigned by default
- Live search + pagination
- Product detail drawer with quantity selector
- Shopping cart (persisted in localStorage)
- Guest checkout flow — user registers + order is placed in one step
- Returning customer login + order placement
- Sales Orders created directly in ERPNext
- Store Settings singleton for price list, tax template, warehouse, etc.

---

## Installation

```bash
# 1. Get the app
bench get-app https://github.com/yourorg/erpnext_store

# 2. Install on your site
bench --site yoursite.com install-app erpnext_store

# 3. Run migrations (creates the DocTypes)
bench --site yoursite.com migrate

# 4. Build assets
bench build --app erpnext_store

# 5. Restart
bench restart
```

The store is now live at `https://yoursite.com/store`.

---

## Configuration

### Store Settings (singleton)
Go to **ERPNext Store > Store Settings** and fill in:

| Field | Description |
|---|---|
| Store Name | Displayed in the navbar and hero |
| Tagline | Subtitle in the hero section |
| Company | ERPNext Company for Sales Orders |
| Price List | Used to pull selling prices (default: Standard Selling) |
| Tax Template | Applied to every Sales Order |
| Default Warehouse | Set on each Sales Order line |
| Currency | Display currency |
| Require Login to Order | Toggle guest checkout on/off |

### Store Categories
Go to **ERPNext Store > Store Category** and create categories.

- **Category Name** — must match an ERPNext **Item Group** name exactly (products are filtered by Item Group)
- **Icon** — any [Tabler Icons](https://tabler.io/icons) class, e.g. `ti-shirt`, `ti-device-laptop`. Leave blank for a random icon.
- **Sort Order** — controls sidebar ordering
- **Active** — toggle visibility

### Products
Products are standard ERPNext **Items** with:
- `Is Sales Item = Yes`
- `Disabled = No`
- An **Item Price** in the configured Price List

Set the Item's **Item Group** to match a Store Category name.

---

## File Structure

```
erpnext_store/
├── setup.py
├── requirements.txt
└── erpnext_store/
    ├── hooks.py                  # App hooks, routes, assets
    ├── api.py                    # Whitelisted API endpoints
    ├── modules.txt
    ├── www/
    │   ├── store.html            # Served at /store
    │   └── store.py             # Page context (store name, no_cache)
    ├── public/
    │   ├── css/store.css        # Storefront styles
    │   └── js/store.js          # Vanilla JS SPA
    └── doctype/
        ├── store_category/
        │   ├── store_category.json
        │   └── store_category.py   # Auto-assigns random icon
        └── store_settings/
            ├── store_settings.json
            └── store_settings.py
```

---

## API Reference

All endpoints are under `erpnext_store.api.*` and called via `frappe.call()`.

| Method | Auth | Description |
|---|---|---|
| `get_store_settings` | Guest | Returns store name, tagline, currency |
| `get_categories` | Guest | Returns active Store Categories |
| `get_products` | Guest | Paginated, filterable product list |
| `get_product` | Guest | Single product detail |
| `register_and_place_order` | Guest | Creates User + Customer + Sales Order |
| `login_and_place_order` | Guest | Authenticates existing user + Sales Order |

---

## Customisation Tips

- **Styling** — edit `public/css/store.css`. All colours use CSS variables at the top.
- **Icons** — the default random pool is in `store_category.py → DEFAULT_ICONS`. Extend it freely.
- **Hero** — edit the `store-hero` block in `store.js → renderHero()`.
- **Additional order fields** — extend `api.py → register_and_place_order` to capture address, notes, etc.
