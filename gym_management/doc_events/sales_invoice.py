import frappe
from frappe.model.document import Document

def update_status_in_membership(doc, method):
    if doc.docstatus == 1 and doc.status == "Paid":
        if doc.custom_membership:
            membership = frappe.get_doc("Membership", doc.custom_membership)
            membership.payment_status = "Paid"
            memmbership.invoice = doc.name
            membership.save()
            frappe.msgprint(f"Membership {membership.name} status updated to Paid.")