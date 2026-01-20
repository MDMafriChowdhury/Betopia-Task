# Automatic Payment Reconciliation via Sales Order Reference

**Technical Assessment - Task 1**

## **Overview**

This module automates the reconciliation process between Customer Payments (Journal Entries) and Customer Invoices. It intercepts the posting of a payment, detects a Sales Order (SO) reference in the journal item label, and automatically links the payment to the corresponding unpaid invoices.

## **Features**

* **Dynamic SO Detection:** Identifies Sales Order numbers (e.g., `S00045`) in the payment label without regex hardcoding.

* **Automatic Reconciliation:** Matches payments to open invoices derived from the identified Sales Order.

* **Partial Payment Support:** Handles cases where the payment amount is less than the invoice total.

* **Multi-Invoice Handling:** Capable of reconciling a single payment across multiple invoices linked to the same SO.

* **Bank Statement Compatibility:** Works for both manual Journal Entries and imported Bank Statement lines.

## **Technical Implementation**

### **1. The Hook: `_post()` Override**

The logic is triggered by overriding the `_post()` method in `account.move`. This ensures that reconciliation only occurs when a transaction is officially confirmed (transition from `draft` -> `posted`), maintaining data integrity.

### **2. Detection Logic (Constraint Compliance)**

* **Requirement:** "No Hardcoded Sales Order number formats."

* **Solution:** The system uses `re.split()` to tokenise the label string (e.g., "Payment for S00001") and verifies tokens against the `sale.order` database. It does not rely on a fixed pattern like `^SO\d+$`.

### **3. Performance (Constraint Compliance)**

* **Requirement:** "No brute-force ORM loops over invoices."

* **Solution:** Instead of iterating through all open invoices, the system performs a targeted SQL search (`search()` domain) to fetch only the invoices linked to the specific Sales Order found.

### **4. Reconciliation Flow**

1. **Identify:** The system extracts potential references from the first journal item's label.

2. **Search:** It verifies if a valid `sale.order` exists for that reference.

3. **Match:** It retrieves `posted` invoices linked to that SO with a payment state of `not_paid` or `partial`.

4. **Reconcile:** It isolates the `asset_receivable` lines from both the Payment and the Invoice and calls Odoo's native `reconcile()` method.

## **Installation & Usage**

### **Prerequisites**

* **Odoo 19** (Community or Enterprise)

* Depends on: `account`, `sale`

### **Testing the Workflow**

1. **Create a Sales Order:** Create and confirm a new SO (e.g., `S00005`).

2. **Create an Invoice:** Generate and post an invoice for that SO. Ensure it is Unpaid.

3. **Create a Payment:**

   * Go to **Accounting/Invoicing** > **Journal Entries** > **New**.

   * Select a **Bank Journal**.

   * Add a line for **Account Receivable**:

     * **Partner:** Must match the Invoice Customer.

     * **Label:** Enter text containing the SO number (e.g., `Wire Transfer for S00005`).

     * **Credit:** Enter the payment amount.

   * Add a balancing line for the Bank Account.

4. **Post:** Click **Post**.

5. **Verify:** Return to the Invoice. The status will have automatically changed to **PAID** (or **Partial**).

## **File Structure**

```text
payment_so_reconciliation/
├── __init__.py
├── __manifest__.py
├── README.md
└── models/
    ├── __init__.py
    └── account_move.py  # Core logic implementation