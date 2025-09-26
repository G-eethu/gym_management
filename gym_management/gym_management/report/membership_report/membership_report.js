// Copyright (c) 2025, Geethu K and contributors
// For license information, please see license.txt

frappe.query_reports["Membership Report"] = {
    "filters": [
        {
            "fieldname": "membership",
            "label": __("Membership"),
            "fieldtype": "Link",
            "options": "Membership",
            "reqd": 0
        }
    ]
};

