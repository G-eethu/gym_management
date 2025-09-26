# Copyright (c) 2025, Geethu K and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": "Membership ID", "fieldname": "membership", "fieldtype": "Link", "options": "Membership", "width": 160},
        {"label": "Member ID", "fieldname": "member_id", "fieldtype": "Data", "width": 140},
        {"label": "Member Name", "fieldname": "member_name", "fieldtype": "Data", "width": 160},
        {"label": "Membership Plan", "fieldname": "membership_plan", "fieldtype": "Data", "width": 140},
        {"label": "Start Date", "fieldname": "start_date", "fieldtype": "Date", "width": 120},
        {"label": "End Date", "fieldname": "end_date", "fieldtype": "Date", "width": 120},
        {"label": "Invoice", "fieldname": "invoice", "fieldtype": "Link", "options": "Sales Invoice", "width": 180},  
        {"label": "Invoice Date", "fieldname": "invoice_date", "fieldtype": "Date", "width": 120},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 120},
        {"label": "Invoice Status", "fieldname": "invoice_status", "fieldtype": "Data", "width": 120},
    ]


def get_data(filters):
    conditions = ""
    if filters.get("membership"):
        conditions += f" and m.name = '{filters.get('membership')}' "

    query = f"""
        SELECT 
            m.name as membership,
            m.member_id as member_id,
            m.full_name as member_name,
            m.membership_plan as membership_plan,
            m.start_date as start_date,
            m.end_date as end_date,
            si.name as invoice,
            si.posting_date as invoice_date,
            si.grand_total as amount,
            si.status as invoice_status
        FROM `tabMembership` m
        LEFT JOIN `tabSales Invoice` si ON si.custom_membership = m.name
        WHERE 1=1 {conditions}
        ORDER BY si.posting_date DESC
    """

    return frappe.db.sql(query, as_dict=True)
