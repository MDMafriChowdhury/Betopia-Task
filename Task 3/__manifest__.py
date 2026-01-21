{
    'name': 'Employee Letter Generation Wizard',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Generate and customize dynamic employee letters (Appointment, Promotion, etc.)',
    'description': """
    Task 3: Dynamic Employee Letter Generation Wizard
    
    Features:
    - Configuration model to define Letter Types (linked to QWeb Views).
    - Single Wizard to select Employee and Letter Type.
    - Auto-populates data (Name, Dept, Job, etc.) into the template.
    - Live HTML Preview: The QWeb template is rendered into an editable HTML field.
    - PDF Generation: Prints exactly what is in the preview.
    - Includes default templates for Appointment and Promotion letters.
    """,
    'depends': ['hr', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'data/default_templates.xml',
        'data/default_letter_types.xml',
        'views/letter_type_view.xml',
        'wizard/letter_generator_view.xml',
        'report/letter_report.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}