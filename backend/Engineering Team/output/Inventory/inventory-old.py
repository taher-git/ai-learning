import logging
import json
from reportlab.pdfgen import canvas

class InventoryItem:
    def __init__(self, item_id, name, category, quantity, price, supplier, reorder_threshold):
        self.item_id = item_id
        self.name = name
        self.category = category
        self.quantity = quantity
        self.price = price
        self.supplier = supplier
        self.reorder_threshold = reorder_threshold


class InventoryManager:
    def __init__(self):
        self.inventory = []
        self.audit_logs = []

    def add_item(self, item):
        # Add an item to the inventory with proper validations
        if self._validate_item(item):
            self.inventory.append(item)
            self._add_audit_log("ADD", item)
            return 'Item added successfully'
        else:
            return 'Invalid item data'

    def update_item(self, item_id, new_item_data):
        # Update an existing item in the inventory
        for item in self.inventory:
            if item.item_id == item_id:
                item.__dict__.update(new_item_data)
                self._add_audit_log("UPDATE", item)
                return 'Item updated successfully'
        return 'Item not found'

    def delete_item(self, item_id):
        # Delete an item from the inventory
        for item in self.inventory:
            if item.item_id == item_id:
                self.inventory.remove(item)
                self._add_audit_log("DELETE", item)
                return 'Item deleted successfully'
        return 'Item not found'

    def view_item(self, item_id):
        # View details of a specific item in the inventory
        for item in self.inventory:
            if item.item_id == item_id:
                return item.__dict__
        return 'Item not found'

    def search_items(self, key, value):
        # Search for items in the inventory based on a specific key and value
        results = []
        for item in self.inventory:
            if getattr(item, key) == value:
                results.append(item.__dict__)
        return results

    def generate_report(self, report_type):
        # Generate inventory reports in PDF format based on the report type
        if report_type == 'low_stock':
            low_stock_items = [item.__dict__ for item in self.inventory if item.quantity < item.reorder_threshold]
            pdf = canvas.Canvas("low_stock_report.pdf")
            for index, item in enumerate(low_stock_items, start=1):
                pdf.drawString(10, 800 - index*20, json.dumps(item))
            pdf.save()
            return 'Low stock report generated successfully'
        elif report_type == 'total_value':
            total_value = sum(item.quantity * item.price for item in self.inventory)
            pdf = canvas.Canvas("total_inventory_value_report.pdf")
            pdf.drawString(10, 800, f'Total Inventory Value: {total_value}')
            pdf.save()
            return 'Total inventory value report generated successfully'
        else:
            return 'Invalid report type'

    def _validate_item(self, item):
        # Perform validations on the item data
        if not all([item.item_id, item.name, item.category, item.quantity, item.price, item.supplier, item.reorder_threshold]):
            return False
        return True

    def _add_audit_log(self, action, item):
        # Maintain audit logs for all CRUD operations
        self.audit_logs.append({'action': action, 'item': item.__dict__})

inventory_manager = InventoryManager()
item1 = InventoryItem('001', 'Chair', 'Furniture', 100, 50, 'SupplierA', 20)
print(inventory_manager.add_item(item1))
print(inventory_manager.inventory)
new_item_data = {'quantity': 120}
print(inventory_manager.update_item('001', new_item_data))
print(inventory_manager.view_item('001'))
print(inventory_manager.search_items('category', 'Furniture'))
print(inventory_manager.generate_report('total_value'))