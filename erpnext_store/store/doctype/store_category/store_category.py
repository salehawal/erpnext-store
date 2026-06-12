import frappe
from frappe.model.document import Document

# Default icons pool — assigned randomly when no icon is set
DEFAULT_ICONS = [
    "ti-shirt", "ti-device-laptop", "ti-home", "ti-tool",
    "ti-truck", "ti-heart", "ti-book", "ti-camera",
    "ti-music", "ti-sports", "ti-plant", "ti-cube",
    "ti-gift", "ti-bath", "ti-building-store", "ti-pizza",
]


class StoreCategory(Document):
    def before_save(self):
        if not self.icon:
            import random
            self.icon = random.choice(DEFAULT_ICONS)
