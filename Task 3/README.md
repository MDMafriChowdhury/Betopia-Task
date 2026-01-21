# Dynamic Employee Letter Generator Wizard

**Technical Assessment - Task 3**

## **Overview**
This module provides a flexible HR tool to generate, preview, customize, and print official employee letters (e.g., Appointment Letters, Promotion Letters) directly from Odoo. It leverages Odoo's QWeb templating engine to ensure consistent formatting while allowing on-the-fly customization by HR officers.

## **Features**
* **Configuration-Driven Templates:** Administrators can define new Letter Types and link them to specific QWeb Views, allowing for unlimited template variations without changing Python code.
* **Live HTML Preview:** Select an employee and a template to instantly see a rendered preview populated with real database values (Name, Department, Job Position, Dates).
* **WYSIWYG Editing:** The preview content is editable. HR officers can tweak specific wording or add bonuses before generating the final PDF.
* **PDF Export:** Generates a professional PDF that exactly matches the preview content.
* **Odoo 19 Compatible:** Built using the latest Odoo 19 syntax (e.g., `<list>` views) and safe dependency checks.

## **Technical Implementation**

### **1. Architecture: Separation of Concerns**
* **Model (`hr.letter.type`):** Stores the configuration. It links a human-readable name (e.g., "Promotion") to a technical `ir.ui.view` (QWeb).
* **Wizard (`hr.letter.generator`):** Handles the transaction. It combines the *Data* (Employee) with the *Template* (View) to produce the *Output* (HTML/PDF).

### **2. Dynamic QWeb Rendering**
Instead of hardcoding strings in Python, we use Odoo's native rendering engine:
```python
rendered_html = self.env['ir.qweb']._render(view_id, values)