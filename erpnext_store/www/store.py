import frappe


def get_context(context):
    settings = frappe.get_single("Store Settings")
    context.store_name = settings.store_name or "Store"
    context.store_tagline = settings.store_tagline or ""
    context.no_cache = 1  # always fresh
