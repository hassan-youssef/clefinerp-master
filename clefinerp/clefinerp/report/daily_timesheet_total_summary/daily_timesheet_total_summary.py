# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt




from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.desk.reportview import build_match_conditions

def execute(filters=None):
	if not filters:
		filters = {}
	elif filters.get("from_date") or filters.get("to_date"):
		filters["from_time"] = "00:00:00"
		filters["to_time"] = "24:00:00"

	columns = get_column()
	conditions = get_conditions(filters)
	data = get_data(conditions, filters)

	return columns, data

def get_column():
	return [_("Employee Name") + "::150",_("Project Name") + "::150", _("Task Subject") + "::150", 
		_("From Datetime") + "::140", _("To Datetime") + "::140", _("Hours") + "::70", 
		_("Activity Type") + "::120", _("Task") + ":Link/Task:150",
		_("Project") + ":Link/Project:120", _("Status") + "::70", _("Employee") + "::150",_("Timesheet") + ":Link/Timesheet:120"]

def get_data(conditions, filters):
	time_sheet = frappe.db.sql(""" 
		SELECT `tabTimesheet`.employee_name, `tabProject`.project_name,`tabTask`.subject,
			`tabTimesheet Detail`.from_time, `tabTimesheet Detail`.to_time, `tabTimesheet Detail`.hours,
			`tabTimesheet Detail`.activity_type, `tabTimesheet Detail`.task, `tabTimesheet Detail`.project,
			`tabTimesheet`.status 
			, `tabTimesheet`.employee, `tabTimesheet`.name
		FROM	`tabTimesheet Detail` LEFT OUTER JOIN `tabTimesheet` ON `tabTimesheet Detail`.parent = `tabTimesheet`.name 
				LEFT OUTER JOIN `tabProject` ON  `tabProject`.name = `tabTimesheet Detail`.project
				LEFT OUTER JOIN `tabTask` ON `tabTask`.name = `tabTimesheet Detail`.task

		WHERE %s order by `tabTimesheet Detail`.from_time ASC """%(conditions), filters, as_list=1)

	return time_sheet

def get_conditions(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += " `tabTimesheet Detail`.from_time >= timestamp(%(from_date)s, %(from_time)s)"
	if filters.get("to_date"):
		conditions += " and `tabTimesheet Detail`.to_time <= timestamp(%(to_date)s, %(to_time)s)"
	if filters.get("project"):
		conditions += " and `tabProject`.name = %(project)s"
	if filters.get("employee"):
		conditions += " and `tabTimesheet`.employee = %(employee)s"

	match_conditions = build_match_conditions("Timesheet")
	if match_conditions:
		conditions += " and %s" % match_conditions

	return conditions