{
    'name': 'Sales Order Migration Tool (O17 to O19)',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Migrate Sales Orders from Odoo 17 using XML-RPC',
    'description': """
    Task 4: Sales Order Migration from Odoo 17 -> Odoo 19
    
    Features:
    - XML-RPC Connection to Odoo 17.
    - Idempotent migration (prevents duplicates).
    - Preserves Prices, Taxes, and States.
    - Transaction-safe (per-record rollback).
    - Detailed Logging (Migrated, Skipped, Failed).
    - Partner & Product Mapping.
    """,
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/migration_tool_view.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}