// Copyright (c) 2025, Geethu K and contributors
// For license information, please see license.txt

frappe.ui.form.on("Membership", {
	date_of_birth(frm) {
        if (frm.doc.date_of_birth) {
            let age = frappe.datetime.get_diff(frappe.datetime.nowdate(), frm.doc.date_of_birth) / 365;
            frm.doc.ages = Math.floor(age);
            frm.refresh_field('ages');
        }
    },
    refresh(frm) {
        if (frm.doc.date_of_birth) {
            let age = frappe.datetime.get_diff(frappe.datetime.nowdate(), frm.doc.date_of_birth) / 365;
            frm.doc.ages = Math.floor(age);
            frm.refresh_field('ages');
        }
    },
    on_submit(frm) {
        if (frm.doc.ages < 18) {
            frappe.msgprint(__('Member must be at least 18 years old to submit the membership.'));
            frappe.validated = false;
        }
    }
});
