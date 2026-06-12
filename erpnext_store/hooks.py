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
# Static assets — served directly from /assets/erpnext_store/
# These are plain CSS/JS files copied by `bench build` via
# Frappe's asset link step; no esbuild bundling needed.
# They are injected into the page from www/store.html directly.
# ------------------------------------------------------------------
# (No web_include_css / web_include_js here — those trigger esbuild.
#  The store.html template loads the files with <link> / <script> tags.)

# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------
fixtures = [
    {"dt": "Store Category"},
]
