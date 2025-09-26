# Copyright (c) 2025, Geethu K and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import add_months
from frappe.model.document import Document


class Membership(Document):
    def on_submit(self):
        """When membership is submitted, activate the member and create invoice"""
        member = frappe.get_doc("Member", self.member_id)
        member.status = "Active"
        member.membership_id = self.name
        member.save()

        self.create_invoice()

    def create_invoice(self):
        """Create Sales Invoice for this membership and update renewal details"""
        # Ensure Gym Membership item exists
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

        # Create Sales Invoice
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

        # Update renewed_payment_details child table
        # Check if an entry already exists for this invoice
        exists = False
        for row in self.renewed_payment_details:
            if row.sales_invoice == invoice.name:
                row.amount = invoice.grand_total
                row.status = invoice.status
                exists = True
                break

        if not exists:
            self.append("renewed_payment_details", {
                "sales_invoice": invoice.name,
                "amount": invoice.grand_total,
                "status": invoice.status
            })

        self.save(ignore_permissions=True)

        return invoice


@frappe.whitelist()
def renew_membership(membership_name, membership_plan, start_date, end_date, membership_fee):
    """Renew an expired membership by updating its plan, dates, and fee"""
    membership = frappe.get_doc("Membership", membership_name)

    if membership.status != "Expired":
        frappe.throw("Only expired memberships can be renewed.")

    # Update membership details
    membership.membership_plan = membership_plan
    membership.start_date = start_date
    membership.end_date = end_date
    membership.membership_fee = membership_fee
    membership.status = "Active"
    membership.save(ignore_permissions=True)

    # Create new invoice for renewal
    invoice = membership.create_invoice()

    # # Append renewed payment details
    # membership.append("renewed_payment_details", {
    #     "sales_invoice": invoice.name,
    #     "amount": invoice.grand_total
    # })

    # 🔑 Save again after appending child row
    membership.save(ignore_permissions=True)

    return {
        "membership": membership.name,
        "invoice": invoice.name
    }

@frappe.whitelist()
def get_plan_details(membership_plan):
    """Fetch fee and duration from Gym Settings for the given plan"""
    settings = frappe.get_doc("Gym Settings")

    for row in settings.membership_payment:
        if row.membership_plan == membership_plan:
            return {
                "amount": row.amount,
                "plan": row.membership_plan
            }

    return {}


@frappe.whitelist()
def get_available_plans():
    """Return all available membership plans from Gym Settings"""
    settings = frappe.get_doc("Gym Settings")
    return [row.membership_plan for row in settings.membership_payment]
