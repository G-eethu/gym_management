# Copyright (c) 2025, Geethu K and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Member(Document):
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
