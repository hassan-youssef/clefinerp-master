// Copyright (c) 2016, clefincode.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Trial Balance For Party Multicurrency"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": "2021-1-1",
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"account",
			"label": __("Account"),
			"fieldtype": "Link",
			"options": "Account",	
			"get_query": function () {
				return {
					filters: [
						["Account", "company", "=", frappe.query_report.get_filter_value("company")]
					]
				};
			},	
		},
	
		{
			"fieldname": "presentation_currency",
			"label": __("Currency"),
			"fieldtype": "Select",
			"options": erpnext.get_presentation_currency_list(),
			
		},
	]
};

