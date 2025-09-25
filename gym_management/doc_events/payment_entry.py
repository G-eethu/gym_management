import frappe

def update_membership_on_payment(doc, method):
    if doc.doctype == "Payment Entry" and doc.docstatus == 1:
        for ref in doc.references:
            if ref.reference_doctype == "Sales Invoice" and ref.reference_name:
                invoice = frappe.get_doc("Sales Invoice", ref.reference_name)

                # Check if invoice is fully paid
                if invoice.status == "Paid" and invoice.custom_membership:
                    membership = frappe.get_doc("Membership", invoice.custom_membership)
                    membership.payment_status = "Paid"
                    membership.invoice = invoice.name
                    membership.save(ignore_permissions=True)

                    frappe.msgprint(
                        f"Membership {membership.name} updated as Paid (Invoice: {invoice.name})"
                    )
