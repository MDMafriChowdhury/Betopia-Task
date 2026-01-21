Dynamic Employee Letter Generator Wizard

Technical Assessment - Task 3

Overview

This module provides a flexible HR tool to generate, preview, customize, and print official employee letters (e.g., Appointment Letters, Promotion Letters) directly from Odoo. It leverages Odoo's QWeb templating engine to ensure consistent formatting while allowing on-the-fly customization by HR officers before generating the final PDF.

Features

Configuration-Driven Templates: Administrators can define new Letter Types and link them to specific QWeb Views, allowing for unlimited template variations without changing Python code.

Live HTML Preview: Select an employee and a template to instantly see a rendered preview populated with real database values (Name, Department, Job Position, Dates).

WYSIWYG Editing: The preview content is editable. HR officers can tweak specific wording (e.g., adding a specific bonus amount) before generating the final output.

PDF Export: Generates a professional PDF that exactly matches the editable preview content.

Odoo 19 Compatible: Built using the latest Odoo 19 syntax (e.g., <list> views) and robust dependency checks.

Technical Implementation

1. Architecture: Separation of Concerns

The solution strictly separates data, presentation, and logic:

Model (hr.letter.type): Stores configuration. Links a human-readable name to a technical ir.ui.view (QWeb).

Wizard (hr.letter.generator): Handles the transaction. It combines the Data (Employee record) with the Template (QWeb View) to produce the Output (HTML/PDF).

2. Dynamic QWeb Rendering

Instead of hardcoding strings in Python, the module utilizes Odoo's native rendering engine. This supports conditional logic (if/else), loops, and standard Odoo formatting within the templates.

# The wizard dynamically renders the selected view ID using the employee data context
rendered_html = self.env['ir.qweb']._render(view_id, values)


3. The Preview & Print Mechanism

Trigger: An @api.onchange method triggers whenever the Employee or Letter Type is modified.

Storage: The rendered result is stored in a Html field (preview_content) on the wizard.

Report Strategy: The PDF report does not re-fetch data from the database. Instead, it prints the preview_content field directly. This ensures that manual edits made by the user in the wizard are preserved in the final PDF.

4. Robustness & Compatibility

Odoo 19 Syntax: Utilizes the new <list> tag instead of the deprecated <tree> tag for list views.

Safe Dependency Handling: The logic detects if the hr_contract module is installed. If first_contract_date is missing, it gracefully falls back to the employee's creation date to prevent system crashes.

Installation & Usage

Prerequisites

Odoo 19 (Community or Enterprise)

wkhtmltopdf (Required system package for PDF generation)

Depends on: hr (Employees)

Workflow

Configuration (Optional):

Go to Employees > Configuration > Letter Types.

(Default templates for Appointment and Promotion are pre-loaded).

Generate a Letter:

Go to Employees > Generate Letter (or via the Employees top menu).

Select an Employee and a Letter Type.

Customize:

The preview box automatically fills with text.

Edit the text inside the box if specific changes are needed for this employee.

Print:

Click Download PDF.

The downloaded file will match your preview exactly.

File Structure

employee_letter_wizard/
├── models/
│   └── letter_type.py          # Configuration Model linked to ir.ui.view
├── wizard/
│   └── letter_generator.py     # Logic for rendering QWeb to HTML
├── views/
│   └── letter_type_view.xml    # Backend Views (using <list> syntax)
├── data/
│   ├── default_templates.xml   # Standard QWeb Templates
│   └── default_letter_types.xml# Pre-loaded Data Records
└── report/
    └── letter_report.xml       # PDF Report Action definition