###This file is for overriding document events

import frappe
from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note
from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_invoice
from erpnext.buying.doctype.purchase_order.purchase_order import make_purchase_receipt
from erpnext.stock.doctype.purchase_receipt.purchase_receipt import make_purchase_invoice

def on_submit_doc(doc, method=None):
    if (doc.doctype == "Sales Order" or doc.doctype == "Purchase Order") and method == "on_submit":
        if hasattr(doc, "auto_create_delivery_note") and (doc.auto_create_delivery_note == 1 or doc.auto_create_delivery_note == '1'):
            dn = make_delivery_note(doc.name)
            dn.insert(ignore_permissions = True)
            dn.submit()
        elif hasattr(doc, "auto_create_purchase_receipt") and (doc.auto_create_purchase_receipt == 1 or doc.auto_create_purchase_receipt == '1'):
            pr = make_purchase_receipt(doc.name)
            pr.insert(ignore_permissions = True)
            pr.submit()
        

    elif doc.doctype == "Delivery Note" and method == "on_submit":
        sales_order = doc.items[0].get("against_sales_order")
        if sales_order:
            so_doc = frappe.get_doc("Sales Order", sales_order)
            if hasattr(so_doc, "auto_create_sales_invoice"):
                if so_doc.auto_create_sales_invoice == 1 or \
                so_doc.auto_create_sales_invoice == '1':
                    si = make_sales_invoice(doc.name)
                    cost_center = frappe.db.get_value("Project", si.project, "cost_center") if si.project else \
                    frappe.db.get_value("Company", si.company, "cost_center")
                    si.cost_center = cost_center
                    si.insert(ignore_permissions = True)
                    si.submit()
    elif doc.doctype == "Purchase Receipt" and method == "on_submit":
        purchase_order = doc.items[0].get("purchase_order")
        if purchase_order:
            po_doc = frappe.get_doc("Purchase Order", purchase_order)
            if hasattr(po_doc, "auto_create_purchase_invoice"):
                if po_doc.auto_create_purchase_invoice == 1 or \
                po_doc.auto_create_purchase_invoice == '1':
                    pi = make_purchase_invoice(doc.name)
                    cost_center = frappe.db.get_value("Project", pi.project, "cost_center") if pi.project else \
                    frappe.db.get_value("Company", pi.company, "cost_center")
                    pi.cost_center = cost_center
                    pi.insert(ignore_permissions = True)
                    pi.submit()


def validate_doc(doc, method=None):
    if doc.doctype == "Delivery Note":
        sales_order = doc.items[0].against_sales_order
        if sales_order:
            so_doc = frappe.get_doc("Sales Order", sales_order)
            doc.posting_date = so_doc.delivery_date
    elif doc.doctype == "Sales Invoice":
        delivery_note = doc.items[0].delivery_note
        if delivery_note:
            dn_doc = frappe.get_doc("Delivery Note", delivery_note)
            sales_order = dn_doc.items[0].against_sales_order
            so_doc = frappe.get_doc("Sales Order", sales_order)
            doc.posting_date = so_doc.transaction_date
    elif doc.doctype == "Purchase Receipt":
        purchase_order = doc.items[0].get("purchase_order")
        if purchase_order:
            po_doc = frappe.get_doc("Purchase Order", purchase_order)
            doc.posting_date = po_doc.schedule_date
    elif doc.doctype == "Purchase Invoice":
        purchase_receipt = doc.items[0].get("purchase_receipt")
        if purchase_receipt:
            pr_doc = frappe.get_doc("Purchase Receipt", purchase_receipt)
            purchase_order = pr_doc.items[0].get("purchase_order")
            po_doc = frappe.get_doc("Purchase Order", purchase_order)
            doc.posting_date = po_doc.schedule_date