
{
    'name': 'User Profile Change Password',
    'version': '1.0',
    'category': 'Productivity',
    'summary': 'Adds Change Password option to the User Profile menu',
    'description': """
    Task 2: Add "Change Password" Option in User Profile Menu
    
    - Adds a "Change Password" item to the top-right user dropdown.
    - Opens a secure wizard asking for Old Password, New Password, and Confirm Password.
    - Validates the old password and ensures new passwords match.
    - Updates the password securely.
    - Logs the user out immediately after success.
    """,
    'depends': ['web', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/change_password_wizard_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'user_password_menu/static/src/js/user_menu.js',
        ],
    },
    'installable': True,
    'license': 'LGPL-3',
}