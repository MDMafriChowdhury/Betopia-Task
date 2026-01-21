# Odoo Technical Assessment Submission

**Candidate Submission for Odoo Developer Position**\
**Target Version:** Odoo 19 (Master / Nightly)

------------------------------------------------------------------------

## Repository Overview

This repository contains four custom Odoo modules developed as part of a
**Practical Technical Assessment**.

Each module addresses a distinct business requirement, ranging from
**Accounting automation** to **HR utilities** and **data migration**,
with a strong focus on correctness, performance, and Odoo 19
compatibility.

------------------------------------------------------------------------

## Modules & Tasks

  -----------------------------------------------------------------------------------
  Task   Module Name                   Description          Key Tech Stack
  ------ ----------------------------- -------------------- -------------------------
  Task 1 `payment_so_reconciliation`   Automatic            `account.move`,
                                       reconciliation of    `_post()`, ORM search
                                       customer payments to 
                                       invoices by          
                                       detecting Sales      
                                       Order references in  
                                       journal labels       

  Task 2 `user_password_menu`          Adds a secure        JS Registry Patch,
                                       "Change Password"    `authenticate()`,
                                       wizard to the user   `TransientModel`
                                       profile menu         

  Task 3 `employee_letter_wizard`      Dynamic WYSIWYG tool QWeb,
                                       to preview, edit,    `ir.actions.report`,
                                       and print HR letters `<list>` views
                                       (Appointment /       
                                       Promotion)           

  Task 4 `so_migration_tool`           Safe and idempotent  `xmlrpc.client`,
                                       migration of Sales   `savepoint()`,
                                       Orders from Odoo 17  idempotency logic
                                       to Odoo 19 via       
                                       XML-RPC              
  -----------------------------------------------------------------------------------

------------------------------------------------------------------------

## Key Implementation Highlights

### 1. Compliance & Best Practices

-   **Incremental Commits**
    -   Development followed a clean progression:
        -   Structure → Core Logic → UI
    -   Demonstrates traceable and review-friendly commit history
-   **Odoo 19 Compatibility**
    -   All views use the new `<list>` syntax (replacing deprecated
        `<tree>`)
    -   Updated Python APIs used consistently (e.g., `authenticate` vs
        `check_credentials`)
-   **Security**
    -   `sudo()` is used only where strictly required (e.g., password
        change)
    -   Transaction-safe rollbacks implemented using database savepoints

------------------------------------------------------------------------

### 2. Performance & Scalability

-   **Task 1 -- Payment Reconciliation**
    -   Avoided brute-force loops over invoices
    -   Uses targeted domain searches for scalable performance
-   **Task 4 -- Migration Tool**
    -   Implements per-record savepoints
    -   Ensures large migrations continue even if a single record fails
    -   Includes structured logging for audit and debugging

------------------------------------------------------------------------

## Installation Instructions

### 1. Clone the Repository

``` bash
git clone <repo_url>
```

------------------------------------------------------------------------

### 2. Add to Addons Path

Add the repository path to your `odoo.conf`:

``` ini
addons_path = /path/to/odoo/addons,/path/to/this/repo
```

------------------------------------------------------------------------

### 3. Install Dependencies

Ensure the following core Odoo modules are installed:

-   `account` (Invoicing)
-   `sale_management` (Sales)
-   `hr` (Employees)

------------------------------------------------------------------------

### 4. Install Modules

1.  Go to **Apps**
2.  Click **Update App List**
3.  Search for the module names listed above
4.  Click **Activate**

------------------------------------------------------------------------

## Task-Specific Notes

### Task 1 -- Payment Reconciliation

-   **Usage**
    -   Create a Bank Journal Entry

    -   In the label, include a Sales Order reference:

            Payment for S00xxx

    -   Post the entry
-   **Verification**
    -   The related invoice status updates to **Paid** or **Partially
        Paid**

------------------------------------------------------------------------

### Task 2 -- Change Password

-   **Usage**
    -   Click the User Avatar (top-right)
    -   Select **Change Password**
-   **Security Note**
    -   Forces logout after successful password change

------------------------------------------------------------------------

### Task 3 -- Letter Generator

-   **Usage**
    -   Navigate to:

            Employees → Generate Letter
-   **Prerequisite**
    -   Requires `wkhtmltopdf` installed for PDF generation

------------------------------------------------------------------------

### Task 4 -- Migration Tool

-   **Usage**
    -   Navigate to:

            Sales → Migration Tool
-   **Note**
    -   Requires access to a running Odoo 17 instance
    -   Supports repeatable, idempotent migrations

------------------------------------------------------------------------

## Final Notes

-   All modules are designed to be **production-safe**
-   Emphasis placed on:
    -   Data integrity
    -   Performance
    -   Maintainability
-   Code follows standard Odoo architectural and security practices

------------------------------------------------------------------------

**Status:** Technical assessment complete and ready for review
