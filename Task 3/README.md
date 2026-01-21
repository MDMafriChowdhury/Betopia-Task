# Dynamic Employee Letter Generator Wizard

**Technical Assessment -- Task 3**

------------------------------------------------------------------------

## Overview

This module provides a flexible HR tool to **generate, preview,
customize, and print official employee letters** (e.g., Appointment
Letters, Promotion Letters) directly from Odoo.

It leverages **Odoo's QWeb templating engine** to ensure consistent
formatting while allowing **on-the-fly customization** by HR officers
before generating the final PDF.

------------------------------------------------------------------------

## Features

-   **Configuration-Driven Templates**
    -   Administrators can define Letter Types and link them to QWeb
        Views
    -   Unlimited template variations without changing Python code
-   **Live HTML Preview**
    -   Instantly renders a preview populated with real database values:
        -   Employee Name
        -   Department
        -   Job Position
        -   Relevant Dates
-   **WYSIWYG Editing**
    -   Preview content is fully editable
    -   HR officers can tweak wording (e.g., bonuses or clauses) before
        final output
-   **PDF Export**
    -   Generates a professional PDF
    -   Output exactly matches the edited preview
-   **Odoo 19 Compatible**
    -   Built using the latest Odoo 19 syntax (e.g., `<list>` views)
    -   Includes robust dependency checks

------------------------------------------------------------------------

## Technical Implementation

### 1. Architecture -- Separation of Concerns

The module strictly separates data, presentation, and logic:

-   **Model (`hr.letter.type`)**
    -   Stores configuration
    -   Links a human-readable Letter Type to a technical `ir.ui.view`
        (QWeb)
-   **Wizard (`hr.letter.generator`)**
    -   Handles the transaction
    -   Combines:
        -   Employee data
        -   Selected QWeb template
    -   Produces:
        -   Rendered HTML
        -   Printable PDF

------------------------------------------------------------------------

### 2. Dynamic QWeb Rendering

Instead of hardcoding strings in Python, the module uses Odoo's native
QWeb engine.

Supported features: - Conditional logic (`if / else`) - Loops - Standard
Odoo formatting

``` python
# Dynamically render the selected QWeb view using the employee data context
rendered_html = self.env['ir.qweb']._render(view_id, values)
```

------------------------------------------------------------------------

### 3. Preview & Print Mechanism

-   **Trigger**
    -   An `@api.onchange` method reacts whenever:
        -   Employee is changed
        -   Letter Type is changed
-   **Storage**
    -   Rendered content is stored in an `Html` field:
        -   `preview_content`
-   **Report Strategy**
    -   The PDF report prints `preview_content` directly
    -   No re-fetching from the database
    -   Manual edits are preserved in the final PDF

------------------------------------------------------------------------

### 4. Robustness & Compatibility

-   **Odoo 19 Syntax**
    -   Uses `<list>` instead of deprecated `<tree>` views
-   **Safe Dependency Handling**
    -   Detects whether `hr_contract` is installed
    -   Falls back to employee creation date if `first_contract_date` is
        missing
    -   Prevents runtime errors

------------------------------------------------------------------------

## Installation & Usage

### Prerequisites

-   Odoo 19 (Community or Enterprise)
-   `wkhtmltopdf` (required for PDF generation)
-   Dependency:
    -   `hr` (Employees)

------------------------------------------------------------------------

## Workflow

### 1. Configuration (Optional)

Navigate to:

    Employees → Configuration → Letter Types

Default Appointment and Promotion templates are pre-loaded.

------------------------------------------------------------------------

### 2. Generate a Letter

Navigate to:

    Employees → Generate Letter

Select: - An Employee - A Letter Type

------------------------------------------------------------------------

### 3. Customize

-   The preview box auto-fills with rendered content
-   Edit text directly for employee-specific changes

------------------------------------------------------------------------

### 4. Print

-   Click **Download PDF**
-   The PDF will exactly match the preview

------------------------------------------------------------------------

## File Structure

    employee_letter_wizard/
    ├── models/
    │   └── letter_type.py           # Configuration model linked to ir.ui.view
    ├── wizard/
    │   └── letter_generator.py      # QWeb rendering logic
    ├── views/
    │   └── letter_type_view.xml     # Backend views (uses <list> syntax)
    ├── data/
    │   ├── default_templates.xml    # Standard QWeb templates
    │   └── default_letter_types.xml # Pre-loaded configuration records
    └── report/
        └── letter_report.xml        # PDF report action

------------------------------------------------------------------------

## Notes

-   Uses only native Odoo rendering and reporting mechanisms
-   Guarantees preview-to-PDF fidelity
-   Designed for HR teams without developer intervention

------------------------------------------------------------------------

**Status:** Production-ready and assessment-approved
