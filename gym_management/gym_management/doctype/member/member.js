// Copyright (c) 2025, Geethu K and contributors
// For license information, please see license.txt

frappe.ui.form.on("Member", {
    date_of_birth(frm) {
        frm.doc.age = frappe.datetime.get_diff(frappe.datetime.nowdate(), frm.doc.date_of_birth) / 365;
        frm.refresh_field('age');
    },
    refresh(frm) {
        if (frm.doc.docstatus == 1) {
            frm.add_custom_button(__('Membership'), function () {
                frm.call({
                    method: 'create_membership',
                    doc: frm.doc,
                    callback: function (r) {
                        if (r.message) {
                            var doc = frappe.model.sync(r.message);
                            frappe.set_route('Form', doc[0].doctype, doc[0].name);
                        }
                    }

                });
            }, __("Create"));
        }
    }
});
