# Copyright (c) 2025, Geethu K and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Membership(Document):
    def on_submit(self):
        member = frappe.get_doc("Member", self.member_id)
        member.status = "Active"
        member.membership_id = self.name
        member.save()
        self.create_invoice()

    def create_invoice(self):
        # Create the item only if it does not exist
        if not frappe.db.exists("Item", "Gym Membership"):
            item = frappe.get_doc({
                "doctype": "Item",
                "item_code": "Gym Membership",
                "item_name": "Gym Membership",
                "item_group": "Services",
                "standard_rate": self.membership_fee,
                "is_stock_item": 0,
                "is_sales_item": 1,
                "is_purchase_item": 0
            })
            item.insert(ignore_permissions=True)

        # Create the invoice
        invoice = frappe.new_doc("Sales Invoice")
        invoice.customer = self.full_name
        invoice.custom_membership = self.name
        invoice.invoice_date = frappe.utils.nowdate()
        invoice.due_date = frappe.utils.add_days(frappe.utils.nowdate(), 30)
        invoice.membership = self.name
        invoice.append("items", {
            "item_code": "Gym Membership",
            "item_name": "Gym Membership",
            "rate": self.membership_fee,
            "qty": 1
        })
        invoice.insert(ignore_permissions=True)
        invoice.submit()

        return invoice
		
