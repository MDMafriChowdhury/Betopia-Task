# User Profile Change Password Wizard

**Technical Assessment - Task 2**

## **Overview**

This module enhances the Odoo user experience by adding a **"Change Password"** option directly to the top-right user profile menu. It allows users to securely update their password via a dedicated wizard popup without navigating to the backend settings.

## **Features**

* **User Menu Integration:** Adds a seamless entry to the top-right avatar dropdown menu.
* **Secure Wizard:** Opens a popup asking for Current Password, New Password, and Confirmation.
* **Validation Logic:**
    * Verifies the **Current Password** against the database hash.
    * Ensures **New Password** and **Confirmation** match.
* **Security Compliance:**
    * Uses Odoo's native authentication methods (`authenticate`).
    * Encrypts the new password automatically via the ORM.
* **Auto-Logout:** Forces an immediate session termination upon success to ensure security.

## **Technical Implementation**

### **1. Frontend Integration (JavaScript)**

* **Extension Point:** The module patches the `user_menuitems` registry in the web client.
* **Method:** It injects a new item `{ id: 'change_password', ... }` that triggers an `ir.actions.act_window` call to open the wizard.
* **Why JS?** The user menu is rendered by the client-side OWL framework, requiring a JS extension rather than a simple XML view modification.

### **2. Backend Logic (TransientModel)**

* **Model:** `user.change.password.wizard` (TransientModel).
* **Reasoning:** Since password change requests are temporary transactional data, a `TransientModel` is used. This prevents database bloat as records are automatically vacuumed by Odoo.

### **3. Odoo 19 Compatibility Fix (Authentication)**

* **Challenge:** In Odoo 19 (Master), the internal `check_credentials()` method was removed/refactored, causing `AttributeError` or `TypeError`.
* **Solution:** We implemented the public **`authenticate()`** method.
    ```python
    self.env['res.users'].authenticate(db, login, password)
    ```
    This ensures robust, version-safe password verification that respects Odoo's security stack.

### **4. Security Handling**

* **Privilege Elevation:** Users generally do not have write access to the sensitive `password` field in `res.users`.
* **Implementation:** The wizard uses `user.sudo().write(...)` to bypass record rules strictly for this specific operation, ensuring users can update their own credentials without needing Admin rights.

## **Installation & Usage**

### **Prerequisites**

* **Odoo 19** (Community or Enterprise)
* Depends on: `web`, `base`

### **Testing the Workflow**

1. **Install** the module `user_password_menu`.
2. **Refresh** the browser (crucial for loading the new JavaScript).
3. Click the **User Avatar** in the top-right corner.
4. Select **Change Password**.
5. **Enter Data:**
   * *Current Password:* (Enter wrong one to test validation).
   * *New Password:* (Enter mismatching ones to test validation).
6. **Success:** Enter valid data and click **Change Password**.
7. **Result:** You will be immediately logged out. Log in again with the new credentials.

## **File Structure**

```text
user_password_menu/
├── __init__.py
├── __manifest__.py
├── README.md
├── security/
│   └── ir.model.access.csv      # Access rights for the wizard
├── static/
│   └── src/
│       └── js/
│           └── user_menu.js     # JS Registry Patch
└── wizard/
    ├── change_password_wizard.py       # Python Logic
    └── change_password_wizard_view.xml # XML Popup View