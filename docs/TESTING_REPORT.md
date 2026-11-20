# PEACOCK – Testing Report

## 1. Automated Test Suite Summary
The Peacock application includes an automated test suite executed with `pytest` and `fastapi.testclient.TestClient`.

- **Test Framework:** Pytest 8.3.5
- **Total Test Cases:** 29 passed, 0 failed
- **Execution Time:** ~1.46 seconds
- **Pass Rate:** 100%

---

## 2. Test Execution Log

| Test Module | Test Case | Target Feature | Result |
| :--- | :--- | :--- | :--- |
| `test_auth_rbac.py` | `test_login_invalid_credentials` | Authentication rejection on invalid password | **PASSED** |
| `test_auth_rbac.py` | `test_login_valid_admin` | Admin authentication & session cookie issuance | **PASSED** |
| `test_auth_rbac.py` | `test_login_valid_customer` | Customer authentication & session cookie issuance | **PASSED** |
| `test_auth_rbac.py` | `test_unauthenticated_protected_route_redirects` | Session guard redirection to `/login` | **PASSED** |
| `test_auth_rbac.py` | `test_customer_cannot_access_admin_dashboard` | RBAC guard blocking customer from `/admin/*` | **PASSED** |
| `test_auth_rbac.py` | `test_admin_can_access_admin_dashboard` | Super Admin authorized route access | **PASSED** |
| `test_bookings_conflicts.py` | `test_booking_cost_calculation_and_budget_creation` | Financial arithmetic & automated budget creation | **PASSED** |
| `test_bookings_conflicts.py` | `test_overlapping_confirmed_booking_is_prevented` | Concurrency check blocking overlapping date/time | **PASSED** |
| `test_budget_tracking.py` | `test_budget_calculations_and_recalculation` | Expense addition and remaining balance decrement | **PASSED** |
| `test_encryption.py` | `test_encryption_decryption_cycle` | Fernet authenticated encryption/decryption | **PASSED** |
| `test_encryption.py` | `test_encryption_idempotence` | Idempotent encryption preventing double-wrapping | **PASSED** |
| `test_encryption.py` | `test_decryption_fallback_on_plaintext` | Graceful fallback on unencrypted plaintext | **PASSED** |
| `test_encryption.py` | `test_blind_index_consistency` | HMAC-SHA256 blind indexing for exact searches | **PASSED** |
| `test_payments_workflow.py` | `test_kpay_payment_submission_and_verification_workflow` | KBZPay slip submission & admin approval workflow | **PASSED** |
| `test_public.py` | `test_home_page` | Home page rendering & hero component | **PASSED** |
| `test_public.py` | `test_venues_list` | Venues catalog page | **PASSED** |
| `test_public.py` | `test_venue_detail` | Venue detail page & availability checker | **PASSED** |
| `test_public.py` | `test_packages_page` | Packages catalog page | **PASSED** |
| `test_public.py` | `test_services_page` | Vendors and wedding services showcase | **PASSED** |
| `test_public.py` | `test_about_page` | About us page | **PASSED** |
| `test_public.py` | `test_contact_page` | Contact inquiry form | **PASSED** |
| `test_public.py` | `test_digital_invitation_view_and_rsvp` | Public digital card view & guest RSVP submission | **PASSED** |
| `test_public.py` | `test_availability_api` | Live availability AJAX JSON endpoint | **PASSED** |
| `test_reports_exports.py` | `test_admin_reports_page` | Reports portal rendering | **PASSED** |
| `test_reports_exports.py` | `test_export_bookings_csv` | CSV bookings generation | **PASSED** |
| `test_reports_exports.py` | `test_export_payments_csv` | CSV payments transaction generation | **PASSED** |
| `test_reports_exports.py` | `test_export_bookings_pdf` | PDF report binary rendering via ReportLab | **PASSED** |
| `test_reports_exports.py` | `test_export_payments_pdf` | PDF payments report binary rendering | **PASSED** |
| `test_seating_planner.py` | `test_seating_assignment_and_capacity_constraints` | Table capacity constraint validation | **PASSED** |
