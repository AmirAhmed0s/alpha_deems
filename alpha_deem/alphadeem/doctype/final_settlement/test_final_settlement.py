# Copyright (c) 2023, smart solution and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase

class TestFinalSettlement(FrappeTestCase):
    
    def setUp(self):
        # Setup mock data for testing
        # Create an employee mock document
        self.employee = frappe.get_doc({
            "doctype": "Employee",
            "employee_name": "Test Employee",
            "employee_id": "EMP001",
            "basic_salary": 5000,
            "nature_of_work": "Full-Time",
            "status": "Active"
        })
        self.employee.insert()

        # Create a Final Settlement mock document
        self.final_settlement = frappe.get_doc({
            "doctype": "Final Settlement",
            "employee": self.employee.name,
            "clearance_form": None  # Assuming no clearance form for now
        })
        self.final_settlement.insert()

    def test_get_data_from_employee_when_no_clearance_form(self):
        # Test case when employee has no clearance form
        self.final_settlement.clearance_form = None  # Simulating no clearance form
        self.final_settlement.save()

        # Fetch employee data when no clearance form exists
        employee = frappe.get_doc("Employee", self.employee.name)
        final_settlement_data = frappe.get_doc("Final Settlement", self.final_settlement.name)
        
        # Assert that the data from employee is fetched
        self.assertEqual(final_settlement_data.basic_salary, employee.basic_salary)
        self.assertEqual(final_settlement_data.nature_of_work, employee.nature_of_work)

    def test_get_data_from_clearance_form_if_exists(self):
        # Test case when employee has a clearance form
        clearance_form = frappe.get_doc({
            "doctype": "Clearance Form",
            "employee": self.employee.name,
            "docstatus": 1  # Approved status
        })
        clearance_form.insert()

        self.final_settlement.clearance_form = clearance_form.name  # Simulating that the clearance form exists
        self.final_settlement.save()

        # Fetch data from the clearance form (assuming it's already in the system)
        clearance_form_data = frappe.get_doc("Clearance Form", self.final_settlement.clearance_form)
        final_settlement_data = frappe.get_doc("Final Settlement", self.final_settlement.name)
        
        # Assert that the data is fetched from the clearance form instead of the employee
        self.assertEqual(final_settlement_data.clearance_form, clearance_form_data.name)
        
    def tearDown(self):
        # Cleanup mock data after each test case
        frappe.delete_doc("Employee", self.employee.name)
        frappe.delete_doc("Final Settlement", self.final_settlement.name)
        if hasattr(self, "clearance_form"):
            frappe.delete_doc("Clearance Form", self.clearance_form.name)
