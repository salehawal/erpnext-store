app_name = "erpnext_store"
app_title = "ERPNext Store"
app_publisher = "Your Company"
app_description = "Public-facing storefront for ERPNext"
app_email = "dev@yourcompany.com"
app_license = "MIT"

# ------------------------------------------------------------------
# Website routes
# ------------------------------------------------------------------
website_route_rules = [
    {"from_route": "/store", "to_route": "store"},
    {"from_route": "/store/<path:path>", "to_route": "store"},
]

# ------------------------------------------------------------------
# DocTypes created by this app
# ------------------------------------------------------------------
# (defined under erpnext_store/doctype/)

# ------------------------------------------------------------------
# CSS / JS assets bundled into the website
# ------------------------------------------------------------------
web_include_css = ["/assets/erpnext_store/css/store.css"]
web_include_js  = ["/assets/erpnext_store/js/store.js"]

# ------------------------------------------------------------------
# Fixtures — export these doctypes when running bench export-fixtures
# ------------------------------------------------------------------
fixtures = [
    {"dt": "Store Category"},
]

# ------------------------------------------------------------------
# Permissions
# ------------------------------------------------------------------
# Guest users can call whitelisted API methods; no extra roles needed.
