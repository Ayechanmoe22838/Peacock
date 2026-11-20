# PEACOCK – Administrator Manual

This manual details platform management, booking workflows, and financial oversight for Peacock super administrators.

## 1. Administrative Login
- Login URL: `http://127.0.0.1:8000/login`
- Default Super Admin Account:
  - **Email:** `admin@peacock.com`
  - **Password:** `AdminPassword123!`

## 2. Administrator Dashboard
The dashboard displays real-time key performance indicators directly aggregated from the MySQL database:
- **Verified Revenue:** Total cleared payments in MMK.
- **Pending Booking Queue:** Fast access to booking requests awaiting approval.
- **Confirmed Bookings:** Approved events locked against conflicting dates.
- **Registered Customers & Venues:** Platform growth metrics.
- **Visual Analytics:**
  - *Monthly Revenue Trend (Bar Chart)*
  - *Booking Status Distribution (Doughnut Chart)*
  - Both charts automatically adapt text and grid colors when switching themes.

## 3. Booking Management & Approval Workflow
1. Navigate to **Bookings** in the sidebar.
2. Filter bookings by status (`Pending`, `Approved`, `Confirmed`, `Rejected`, `Cancelled`) or search by booking reference.
3. Click **Review** on any booking to view line-item cost breakdowns, guest counts, and special requirements.
4. **Approve Request:** Advances status to `Approved` and triggers customer notification.
5. **Confirm Booking:** Enforces venue calendar lock and creates event schedule outline.
6. **Reject Request:** Enter an explicit reason, releasing the date slot and notifying the customer.

## 4. Payment Verification Queue
1. Open **Payments** in the sidebar.
2. Click **View Receipt** to inspect the customer's uploaded KBZPay transaction slip.
3. Match the transaction ID with your merchant bank statement.
4. Click **Approve** to verify payment. The system automatically credits `paid_amount`, decrements `balance_amount`, creates an audit log, and notifies the bride/groom.
5. If fraudulent or invalid, click **Reject** with documented justification.

## 5. Exporting Management Reports
1. Go to **Reports** in the sidebar.
2. Select your reporting view:
   - *Bookings & Reservations Summary*
   - *Verified Payment Transactions*
3. Click **Export CSV** for Excel and spreadsheet reconciliation.
4. Click **Export Official PDF** for formatted, printable management reports with official timestamps generated via ReportLab.
