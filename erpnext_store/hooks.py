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
# Fixtures
# ------------------------------------------------------------------
fixtures = [
    {"dt": "Store Category"},
]
