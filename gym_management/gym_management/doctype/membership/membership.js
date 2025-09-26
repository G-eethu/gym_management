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
        if (frm.doc.membership_plan == "Monthly") {
            frm.doc.end_date = frappe.datetime.add_months(frm.doc.start_date, 1);
            frm.refresh_field('end_date');
        } else if (frm.doc.membership_plan == "Quarterly") {
            frm.doc.end_date = frappe.datetime.add_months(frm.doc.start_date, 3);
            frm.refresh_field('end_date');
        }
        else if (frm.doc.membership_plan == "Half-Yearly") {
            frm.doc.end_date = frappe.datetime.add_months(frm.doc.start_date, 6);
            frm.refresh_field('end_date');
        }
        else if (frm.doc.membership_plan == "Yearly") {
            frm.doc.end_date = frappe.datetime.add_months(frm.doc.start_date, 12);
            frm.refresh_field('end_date');
        }
        if (frm.doc.date_of_birth) {
            let age = frappe.datetime.get_diff(frappe.datetime.nowdate(), frm.doc.date_of_birth) / 365;
            frm.doc.ages = Math.floor(age);
            frm.refresh_field('ages');
        }
        if (frm.doc.end_date) {
            let today = frappe.datetime.get_today();
            if (frm.doc.end_date <= today && frm.doc.status !== "Expired") {
                frm.set_value("status", "Expired");
                frm.save_or_update();
            }
        }
        if (frm.doc.status === "Expired" && frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Renew Membership'), function () {
                
                let d = new frappe.ui.Dialog({
                    title: 'Renew Membership',
                    fields: [
                        {
                            label: 'Membership Plan',
                            fieldname: 'membership_plan',
                            fieldtype: 'Select',
                            options: ['Monthly', 'Quarterly', 'Half-Yearly', 'Yearly'],
                            reqd: 1
                        },
                        {
                            label: 'Start Date',
                            fieldname: 'start_date',
                            fieldtype: 'Date',
                            default: frappe.datetime.get_today(),
                            reqd: 1
                        },
                        {
                            label: 'End Date',
                            fieldname: 'end_date',
                            fieldtype: 'Date',
                            reqd: 1
                        },
                        {
                            label: 'Membership Fee',
                            fieldname: 'membership_fee',
                            fieldtype: 'Currency',
                            reqd: 1
                        }
                    ],
                    primary_action_label: 'Renew',
                    primary_action(values) {
                        frappe.call({
                            method: "gym_management.gym_management.doctype.membership.membership.renew_membership",
                            args: {
                                membership_name: frm.doc.name,
                                membership_plan: values.membership_plan,
                                start_date: values.start_date,
                                end_date: values.end_date,
                                membership_fee: values.membership_fee
                            },
                            callback: function(r) {
                                if (r.message) {
                                    frappe.msgprint("Membership renewed successfully.");
                                    frm.reload_doc();
                                    d.hide();
                                }
                            }
                        });
                    }
                });

                // On plan change → fetch amount & set end_date
                d.fields_dict.membership_plan.df.onchange = () => {
                    let plan = d.get_value("membership_plan");
                    let start_date = d.get_value("start_date") || frappe.datetime.get_today();

                    frappe.call({
                        method: "gym_management.gym_management.doctype.membership.membership.get_available_plans",
                        args: { membership_plan: plan },
                        callback: function(r) {
                            if (r.message) {
                                let fee = r.message.amount;

                                d.set_value("membership_fee", fee);

                                // Auto set end_date based on plan
                                if (plan === "Monthly") {
                                    d.set_value("end_date", frappe.datetime.add_months(start_date, 1));
                                    d.set_value("membership_fee", '1000');
                                } else if (plan === "Quarterly") {
                                    d.set_value("end_date", frappe.datetime.add_months(start_date, 3));
                                    d.set_value("membership_fee", '2500');
                                } else if (plan === "Half-Yearly") {
                                    d.set_value("end_date", frappe.datetime.add_months(start_date, 6));
                                    d.set_value("membership_fee", '5500');
                                } else if (plan === "Yearly") {
                                    d.set_value("end_date", frappe.datetime.add_months(start_date, 12));
                                    d.set_value("membership_fee", '10000');
                                }
                            }
                        }
                    });
                };

                d.show();
            }, __("Create"));
        }
    },
    on_submit(frm) {
        if (frm.doc.ages < 18) {
            frappe.msgprint(__('Member must be at least 18 years old to submit the membership.'));
            frappe.validated = false;
        }
    },
    start_date(frm) {
        if (frm.doc.membership_plan == "Monthly") {
            frm.doc.end_date = frappe.datetime.add_months(frm.doc.start_date, 1);
            frm.refresh_field('end_date');
        } else if (frm.doc.membership_plan == "Quarterly") {
            frm.doc.end_date = frappe.datetime.add_months(frm.doc.start_date, 3);
            frm.refresh_field('end_date');
        }
        else if (frm.doc.membership_plan == "Half-Yearly") {
            frm.doc.end_date = frappe.datetime.add_months(frm.doc.start_date, 6);
            frm.refresh_field('end_date');
        }
        else if (frm.doc.membership_plan == "Yearly") {
            frm.doc.end_date = frappe.datetime.add_months(frm.doc.start_date, 12);
            frm.refresh_field('end_date');
        }
    },
    membership_plan: function(frm) {
        if (frm.doc.membership_plan) {
            frappe.db.get_value("Gym Settings", {name: "Gym Settings"}, "membership_payment")
                .then(r => {
                    if (r && r.message) {
                        frappe.db.get_doc("Gym Settings", "Gym Settings").then(doc => {
                            let plan = doc.membership_payment.find(
                                row => row.membership_plan === frm.doc.membership_plan
                            );
                            if (plan) {
                                frm.set_value("membership_fee", plan.amount);
                            } else {
                                frm.set_value("membership_fee", 0);
                            }
                        });
                    }
                });
        } else {
            frm.set_value("membership_fee", 0);
        }
    },
});
