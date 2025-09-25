# Copyright (c) 2025, Geethu K and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Member(Document):
    def on_submit(self):
        self.create_customer()

    def create_customer(self):
        # create new Customer doc
        customer = frappe.new_doc("Customer")
        customer.customer_name = self.full_name
        customer.customer_type = "Individual"
        customer.territory = "All Territories"
        customer.email_id = self.email_id
        customer.mobile_no = self.mobile_number
        customer.date_of_birth = self.date_of_birth
        customer.address = self.address
        customer.gender = self.gender
        customer.save(ignore_permissions=True)



    @frappe.whitelist()
    def create_membership(self):
        # create new Membership doc
        membership = frappe.new_doc("Membership")
        membership.member = self.name
        membership.full_name = self.full_name
        membership.email_id = self.email_id
        membership.mobile_no = self.mobile_number
        membership.start_date = frappe.utils.nowdate()
        membership.end_date = frappe.utils.add_months(frappe.utils.nowdate(), 12)
        membership.date_of_birth = self.date_of_birth
        membership.height = self.height
        membership.weight = self.weight
        membership.address = self.address
        membership.age = self.age
        membership.photo = self.photo
        membership.id_proof = self.id_proof
        membership.emergency_contact = self.emergency_contact_name
        membership.emergency_contact_no = self.emergency_contact_number
        membership.member_id = self.name
        # membership.insert(ignore_permissions=True)

        return membership
