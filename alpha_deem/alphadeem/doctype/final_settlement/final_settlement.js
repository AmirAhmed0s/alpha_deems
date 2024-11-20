// Copyright (c) 2023, smart solution and contributors
// For license information, please see license.txt

frappe.ui.form.on('Final Settlement', {
	refresh: function(frm) {
		frm.events.hidden_zero_field(frm);
		frm.set_query("clearance_form", function () {
			return {
				filters: [
					["docstatus", "=", 1],
				],
			};
		});
	},

	clearance_form: async function(frm) {
		// Check if the employee has a clearance form or not
		if (frm.doc.clearance_form) {
			// If Clearance Form exists, use the data from the Clearance Form
			await frm.call({
				method: "calc_service_duration",
				doc: frm.doc,
				callback: function(r) {
					// Handle any additional logic here if needed
				}
			});
		} else {
			// If Clearance Form does not exist, fetch data from the Employee doctype
			await frm.call({
				method: "get_employee_data",
				doc: frm.doc,
				callback: function(r) {
					// Handle the employee data fetch logic here
					// e.g., populate fields from the Employee doctype if clearance form is absent
				}
			});
		}

		frm.events.hidden_zero_field(frm);
	},

	hidden_zero_field: function(frm) {
		// Hide fields with zero value
		if (frm.doc.extra_work == 0) { frm.set_df_property('extra_work', 'hidden', 1); }
		if (frm.doc.transportation_allowance == 0) { frm.set_df_property('transportation_allowance', 'hidden', 1); }
		if (frm.doc.housing_allowance == 0) { frm.set_df_property('housing_allowance', 'hidden', 1); }
		if (frm.doc.other_allowances == 0) { frm.set_df_property('other_allowances', 'hidden', 1); }
		if (frm.doc.basic_salary == 0) { frm.set_df_property('basic_salary', 'hidden', 1); }
		if (frm.doc.nature_of_work == 0) { frm.set_df_property('nature_of_work', 'hidden', 1); }
	}
});
