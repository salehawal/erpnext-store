from setuptools import setup, find_packages

setup(
    name="erpnext_store",
    version="1.0.0",
    description="ERPNext Storefront — public-facing shop with category browsing, cart, and order submission",
    author="Your Company",
    author_email="dev@yourcompany.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[],
    package_data={
        "erpnext_store": [
            "public/css/*.css",
            "public/js/*.js",
            "www/*.html",
            "www/*.py",
            "templates/**/*.html",
            "doctype/**/*.json",
            "doctype/**/*.py",
            "modules.txt",
            "hooks.py",
        ]
    },
)
