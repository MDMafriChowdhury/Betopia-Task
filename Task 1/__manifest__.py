{
    'name': 'Automatic Payment Reconciliation via SO',
    'version': '1.0',
    'category': 'Accounting/Accounting',
    'summary': 'Auto-reconcile payments based on Sales Order reference in Journal Items',
    'description': """
    Task 1: Automatic Payment Reconciliation Using Sales Order Reference
    
    Identifies Sales Order numbers in the first journal item's label upon posting a move.
    Automatically matches and reconciles the payment with the correct customer invoice(s).
    
    Features:
    - Detects SO number dynamically (no hardcoded formats).
    - Handles partial payments, multiple invoices, and refunds.
    - Works for Journal Entries and Bank Statement Lines.
    """,
    'depends': ['account', 'sale'],
    'data': [],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}