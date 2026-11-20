# MASTER AGENTIC CODING PROMPT
# PEACOCK
## Smart Wedding Reception Management System

---

# 1. ROLE AND RESPONSIBILITY

Act as a Senior Full-Stack Software Engineer, Software Architect, UI/UX Designer, Database Engineer, Backend Developer, Security Engineer, QA Engineer and Technical Documentation Specialist.

Your responsibility is to independently design, develop, implement, test, debug, integrate and document a complete professional web application named:

**PEACOCK – Smart Wedding Reception Management System**

PEACOCK is the official product name.

Build a complete, functional, responsive, secure and database-driven web application.

This is not merely a frontend design, landing page, UI prototype or collection of static dashboard screens.

You must develop an actual working application with a connected backend and MySQL database.

Work as an autonomous agentic development team.

You must:

- Inspect the existing project before modifying it.
- Understand the existing codebase and requirements.
- Create a development plan.
- Design the database and application architecture.
- Implement all required frontend and backend modules.
- Connect every module to MySQL.
- Implement authentication and authorization.
- Implement actual business workflows.
- Test the application continuously.
- Fix errors and integration problems.
- Create complete technical documentation.
- Verify all major functionality before declaring completion.

Do not simply explain how to build the application. Actually work inside the available project workspace.

---

# 2. PROJECT OVERVIEW

## 2.1 Project Description

PEACOCK is a centralized wedding reception management platform that helps customers plan and organize their wedding receptions through one web application.

The application provides:

1. Wedding venue browsing.
2. Wedding package selection.
3. Venue booking.
4. Booking management.
5. Vendor selection.
6. Catering management.
7. Guest management.
8. wedding invitations and reception cards.
9. Seating arrangements.
10. Budget management.
11. Payment management.
12. Event scheduling.
13. Notifications.
14. Feedback management.
15. Reports and analytics.

Administrators manage the entire platform, including customers, venues, bookings, packages, vendors, catering, invitation cards, payments, reports and system settings.

## 2.2 Project Objectives

1. Simplify wedding reception planning.
2. Reduce manual booking and management processes.
3. Provide convenient venue and package selection.
4. Prevent venue booking conflicts.
5. Improve customer and administrator communication.
6. Provide accurate budget and expense tracking.
7. Centralize guest and invitation management.
8. Improve payment record management.
9. Generate meaningful management reports.
10. Provide a user-friendly and secure wedding planning experience.

## 2.3 Main User Roles

The application has two primary roles:

- Admin
- Customer (Wedding Customer)

Implement strict Role-Based Access Control (RBAC).

---

# 3. MANDATORY TECHNOLOGY STACK

Use the following technologies.

## Frontend

- HTML5
- CSS3
- JavaScript

## Backend

- Python 3
- FastAPI
- Uvicorn
-- My SQL

## Database

- MySQL 8.x
- MySQL Workbench
- Alembic for database migrations

## Testing

- Pytest
- FastAPI TestClient
- Appropriate integration and security testing tools

## Development Tools

- Visual Studio Code or Antigravity IDE
- Git and GitHub
- Python Virtual Environment

## Technology Restrictions

Do not replace the requested technology stack with:

- React
- Next.js
- Node.js
- Firebase
- MongoDB
- Django
- Laravel
- Flutter
- Other frontend or backend frameworks.

Use FastAPI for backend functionality and HTML, CSS, JavaScript,  for the frontend.

Do not introduce unnecessary dependencies.

---

# 4. USER ROLES AND FUNCTIONAL REQUIREMENTS

## A. ADMIN ROLE

The Admin manages the overall platform.

### 4.1 Admin Dashboard

Display real database statistics:

- Total registered customers.
- Total active venues.
- Total wedding packages.
- Total invitation/reception cards.
- Total bookings.
- Pending bookings.
- Approved bookings.
- Confirmed bookings.
- Rejected bookings.
- Cancelled bookings.
- Upcoming wedding events.
- Total verified revenue.
- Outstanding payment balances.

Include:

- Booking status chart.
- Monthly revenue chart.
- Recent booking activities.
- Upcoming wedding events.
- Pending booking approvals.
- Recent customer registrations.
- Recent administrative activities.

Use Chart.js with actual database information.

Never use hardcoded dashboard statistics.

### 4.2 User Management

Admin can:

- View all customers.
- Search customers.
- Filter customers.
- View customer details.
- Update customer information.
- Activate accounts.
- Deactivate accounts.
- View customer booking history.
- View registration dates and account status.

### 4.3 Venue Management

Admin can:

- Add venues.
- Edit venue information.
- Delete or deactivate venues.
- Upload multiple venue images.
- Manage descriptions.
- Set venue prices.
- Set venue capacities.
- Manage locations.
- Manage facilities.
- Manage availability.
- View booking history.

Venue information must include:

- Venue name.
- Description.
- Address.
- City.
- Contact information.
- Capacity.
- Base price.
- Facilities.
- Images.
- Active status.
- Created date.
- Updated date.

### 4.4 Venue Availability Management

Admin can:

- View availability calendars.
- Set unavailable dates.
- Manage operating hours.
- Manage available time slots.
- View confirmed bookings.
- Block maintenance dates.
- Prevent overlapping confirmed bookings.

### 4.5 Booking Management

Admin can:

- View booking requests.
- Search and filter bookings.
- View booking details.
- Approve booking requests.
- Reject booking requests.
- Provide rejection reasons.
- Process modification requests.
- Manage cancellation requests.
- View booking payment information.
- Review booking history.

Booking statuses:

- Pending
- Approved
- Confirmed
- Rejected
- Cancellation Requested
- Cancelled
- Completed

Implement valid status transitions.

Every important status change must create an audit record and generate the appropriate customer notification.

### 4.6 Package Management

Admin can:

- Create wedding packages.
- Update packages.
- Delete or deactivate packages.
- Upload package images.
- Set package prices.
- Manage included services.
- Add descriptions.
- Manage package availability.

Package information should include:

- Package name.
- Description.
- Price.
- Included services.
- Guest capacity or pricing rules, where applicable.
- Images.
- Active status.

### 4.7 Vendor Management

Manage wedding service providers such as:

- Photographers.
- Videographers.
- Wedding decorators.
- Florists.
- Entertainment providers.
- Makeup artists.
- Other wedding service providers.

Admin can create, update, view and deactivate vendors.

Vendor information:

- Vendor name.
- Service category.
- Description.
- Contact information.
- Service price.
- Availability.
- Images.
- Active status.

### 4.8 Catering Management

Admin can:

- Add food categories.
- Create menu items.
- Update menu items.
- Delete menu items.
- Manage menu descriptions.
- Manage food prices.
- Manage catering options.
- Manage serving quantities.
- Set availability.

### 4.9 Guest Management

Admin can:

- View guests associated with bookings.
- Search guest records.
- View guest counts.
- View RSVP statistics.

Customers remain responsible for editing their own guest lists.

### 4.10 Invitation and Reception Card Management

Admin can:

- Add invitation templates.
- Upload invitation and reception card designs.
- Edit card information.
- Manage card categories.
- Set card descriptions.
- Set card prices, if applicable.
- Activate or deactivate designs.
- Preview card designs.
- Manage available card templates.

### 4.11 Payment Management

Admin can:

- View payment records.
- View payment details.
- Verify manually submitted payment receipts.
- Approve payments.
- Reject invalid payment submissions.
- Record deposits.
- View outstanding balances.
- View payment history.
- Review refund records.

### 4.12 Report Management

Generate:

- Booking reports.
- Customer reports.
- Venue reports.
- Revenue reports.
- Payment reports.
- Event reports.
- Vendor reports.

Provide date filtering and:

- CSV export.
- PDF export.

Reports must use actual database records.

### 4.13 Feedback Management

Admin can:

- View customer ratings.
- Read reviews.
- Respond to feedback.
- Manage inappropriate reviews.

### 4.14 Notification Management

Admin can:

- Send announcements.
- Notify customers about booking decisions.
- Notify customers about payment verification.
- Send important system updates.

### 4.15 System Settings

Admin can:

- Update website information.
- Manage administrator profiles.
- Manage system configurations.
- View audit logs.
- Manage operational settings.

---

## B. CUSTOMER ROLE

Customers manage their own wedding reception planning.

### 4.16 Registration and Authentication

Customers can:

- Register.
- Log in.
- Log out.
- Reset forgotten passwords.
- Change passwords.

Registration fields:

- Full name.
- Email.
- Phone number.
- Password.
- Confirm password.
- Address.

Requirements:

- Validate email format.
- Enforce unique email addresses.
- Validate phone numbers.
- Validate passwords.
- Securely hash passwords.
- Prevent duplicate registrations.

### 4.17 Profile Management

Customers can:

- View their profiles.
- Update personal information.
- Update contact details.
- Update addresses.
- Change passwords.

### 4.18 Venue Browsing

Customers can:

- Browse active venues.
- Search venues.
- Filter by location.
- Filter by price.
- Filter by capacity.
- View images.
- View facilities.
- View descriptions.
- Check availability.
- View pricing.
- View venue details.

### 4.19 Wedding Package Selection

Customers can:

- Browse packages.
- View package details.
- Compare prices.
- View included services.
- Select packages.
- View package images.

### 4.20 Booking Management

Customers can:

- Select a venue.
- Select a wedding package.
- Choose wedding dates.
- Select start and end times.
- Enter expected guest counts.
- Add special requirements.
- Review estimated costs.
- Submit booking requests.
- View booking history.
- View booking status.
- Request modifications.
- Request cancellations.

### 4.21 Vendor Selection

Customers can:

- Browse vendors.
- Filter by category.
- View vendor details.
- View service prices.
- Select additional vendors.
- View selected vendors.
- Remove selected vendors when allowed.

### 4.22 Catering Management

Customers can:

- Browse food menus.
- View food categories.
- View food descriptions.
- View prices.
- Select menu items.
- Specify quantities.
- Calculate catering costs.
- View selected menus.

### 4.23 Guest Management

Customers can:

- Add guests.
- Update guests.
- Delete guests.
- Search guests.
- Categorize guests.
- View guest counts.
- Track RSVP responses.

Guest information:

- Guest name.
- Phone.
- Email (optional).
- Guest category.
- RSVP status.
- Special requirements.

RSVP statuses:

- Pending
- Accepted
- Declined

### 4.24 Invitation Management

Customers can:

- Browse available invitation and reception card designs.
- Preview card designs.
- Select an invitation template.
- Enter wedding details.
- Enter names of the couple.
- Enter the wedding date and time.
- Enter venue information.
- Enter invitation messages.
- Preview customized invitations.
- Save and edit invitation details.
- View their selected designs.

Only implement actual image generation or PDF creation when the required functionality is available. Otherwise provide a functional template-based design and export workflow.

### 4.25 Seating Arrangement

Customers can:

- Create reception tables.
- Set table names or numbers.
- Set table capacities.
- Assign guests.
- Move guests.
- Remove guest assignments.
- View seating arrangements.

Prevent:

- Assigning guests from another booking.
- Duplicate seating assignments.
- Exceeding table capacity.

Provide an easy-to-understand visual seating interface.

### 4.26 Budget Management

Customers can:

- Set wedding budgets.
- Add expenses.
- Update expenses.
- Delete expenses.
- Categorize expenses.
- View estimated costs.
- View actual expenses.
- View remaining budgets.
- View budget summaries.

Formula:

Remaining Budget = Total Budget - Total Expenses.

Automatically update estimates when selected services change.

### 4.27 Payment Management

Customers can:

- View booking costs.
- View required deposits.
- View payment history.
- View paid amounts.
- View outstanding balances.
- View payment statuses.
- Submit payment references.
- Upload payment receipts.

### 4.28 Event Schedule Management

Customers can:

- Create activities.
- Edit activities.
- Delete activities.
- Set activity times.
- Add descriptions.
- View reception timelines.

Example activities:

- Guest Arrival.
- Welcome Speech.
- Wedding Ceremony.
- Photography.
- Dinner.
- Entertainment.
- Cake Cutting.
- Closing Ceremony.

### 4.29 Notification Management

Customers can:

- Receive booking updates.
- Receive payment updates.
- Receive event reminders.
- View announcements.
- Mark notifications as read.

### 4.30 Feedback Management

Customers can:

- Submit ratings.
- Write reviews.
- View previous feedback.
- View administrator responses.

Only allow feedback for eligible completed bookings.

---

# 5. BUSINESS RULES

Implement the following business rules.

1. Customers must log in before booking.
2. Customers can only access their own private information.
3. Admin-only operations must be protected.
4. Bookings must contain valid venues, dates and times.
5. A venue cannot have overlapping confirmed bookings.
6. Pending bookings must not automatically become confirmed.
7. Only authorized Admin accounts can approve or reject bookings.
8. Booking decisions must generate notifications.
9. Booking costs must include venue, package and additional services.
10. Remaining budget must be calculated automatically.
11. Outstanding balance must equal total booking cost minus verified payments, adjusted for valid refunds.
12. Table capacity must never be exceeded.
13. Guests must belong to the correct booking.
14. Duplicate seating assignments must be prevented.
15. Feedback requires an eligible completed booking.
16. Cancelled bookings must release venue availability.
17. Payment records must preserve transaction history.
18. Payment verification requires authorized Admin action.
19. Customers cannot directly modify approval or payment verification statuses.
20. Financial modifications must be auditable.
21. Customers cannot change their own role to Admin.
22. Venue availability must be checked again when a booking is submitted and approved.
23. Price calculations must be performed on the server, not trusted from frontend values.
24. Booking modification must preserve the original booking history.

Use database transactions and appropriate locking or database constraints to prevent concurrent booking conflicts.

---

# 6. DATABASE DESIGN

Use SQLAlchemy ORM with MySQL 8.x.

Use Alembic for database migrations.

Create normalized database models for:

1. Users
2. Venues
3. VenueImages
4. VenueAvailability
5. Packages
6. PackageServices
7. Bookings
8. Vendors
9. BookingVendors
10. Menus
11. BookingMenus
12. Guests
13. Invitations
14. ReceptionTables
15. SeatingAssignments
16. Budgets
17. Expenses
18. Payments
19. EventSchedules
20. Notifications
21. Feedback
22. AuditLogs
23. InvitationTemplates
24. BookingStatusHistory
25. PaymentHistory
26. SystemSettings

Add any additional tables required by the implemented workflows.

## Database Requirements

- Appropriate primary keys.
- Foreign keys.
- One-to-many relationships.
- Many-to-many relationships.
- Appropriate field types.
- DECIMAL for financial values.
- DATETIME for timestamps.
- Indexes for frequently searched fields.
- Unique constraints.
- Referential integrity.
- created_at and updated_at fields.
- Database transactions.
- Appropriate deletion rules.
- Audit history for financial and booking changes.

Use Myanmar Kyat (MMK) as the initial currency.

Store monetary values using Python Decimal and database DECIMAL types. Never use floating-point arithmetic for financial calculations.

Use consistent timezone handling.

Create complete database relationships and constraints.

Do not put all application information into one database table.

Generate an ER diagram that accurately represents the actual database schema.

---

# 7. KPAY PAYMENT IMPLEMENTATION

Use KPay (KBZPay) as one supported payment method.

Initially implement manual payment verification.

## Customer Workflow

1. Customer opens the payment page.
2. System displays the amount due.
3. System displays configured official payment instructions.
4. Customer makes payment through the supported KPay process.
5. Customer enters the transaction reference.
6. Customer uploads the receipt.
7. System creates a Pending Verification payment record.
8. Admin reviews the receipt and transaction details.
9. Admin approves or rejects the submission.
10. System updates payment status.
11. Customer receives a notification.

Payment statuses:

- Pending
- Pending Verification
- Verified
- Rejected
- Refunded

Important requirements:

- Do not invent KPay APIs.
- Do not pretend payments are automatically verified.
- Only implement automatic verification when authorized API documentation and credentials are available.
- Never store payment PINs, OTPs or banking passwords.
- Protect uploaded receipts.
- Restrict payment receipt access to authorized users.
- Preserve all payment history.
- Prevent duplicate transaction references where appropriate.
- Make verification actions auditable.

---

# 8. BRAND IDENTITY AND UI/UX DESIGN (You can also use ideas or designs from Given folders or Files)

## 8.1 Official Brand

Brand name: PEACOCK

Application title:

Peacock – Smart Wedding Reception Management System.

Create a premium, elegant and modern wedding reception management platform.

Avoid ordinary generic administration templates.

## 8.2 Official Peacock Color Palette

Use these colors consistently.

| Color Name | HEX |
|---|---|
| Royal Peacock Blue | #063B78 |
| Turquoise Blue | #1688C1 |
| Emerald Green | #006B45 |
| Deep Peacock Green | #1B4A35 |
| Leaf Green | #4A7640 |
| Peacock Feather Gold | #C5A76B |
| Dark Emerald | #003B36 |
| Champagne Gold | #D6B875 |
| Ivory Cream | #F1E4C8 |
| Warm Charcoal | #49443F |
| Warm Taupe | #B8B0A0 |

Design rules:

- Use White, Royal Peacock Blue and Deep Peacock Green as major brand colors.
- Use ivory and white for elegant light surfaces.
- Use gold as a premium accent.
- Avoid excessive black backgrounds.
- Avoid excessive saturated colors.
- Maintain readable text and accessible contrast.
- Apply colors consistently across all pages.

## 8.3 Typography

Suggested fonts:

- Playfair Display for selected headings.
- Poppins for interface elements.
- Inter for supporting text.

Use consistent typography and a clear hierarchy.

## 8.4 Visual Design

Implement:

- Elegant spacing.
- Clean layouts.
- Consistent alignment.
- Subtle shadows.
- Rounded corners.
- High-quality wedding photography.
- Clear navigation.
- Premium venue cards.
- Professional forms.
- Consistent icons.
- Subtle transitions.
- Minimal unnecessary animations.

Use the existing Home Page folder as a visual reference if it exists in the workspace.

Preserve appropriate supplied images and assets.

Do not use broken image links or unrelated placeholder photography.

---

# 9. LIGHT MODE AND DARK MODE

Implement application-wide theme switching.

Provide:

1. Light Mode.
2. Dark Mode.

Requirements:

- Add a visible theme toggle in the navigation/header.
- Use appropriate sun and moon icons.
- Switch themes without reloading the page.
- Save the user's preference in localStorage.
- Restore the selected theme when the user returns.
- Support system theme preference where appropriate.
- Avoid theme flashing during initial page loading.
- Provide readable contrast in both themes.

Apply themes across:

- Public website.
- Admin dashboard.
- Customer dashboard.
- Navigation bars.
- Sidebars.
- Cards.
- Forms.
- Tables.
- Modals.
- Dropdowns.
- Charts.
- Notifications.
- Calendar views.
- Payment pages.
- Login and registration pages.

Use centralized CSS theme variables.

Ensure Chart.js charts update their text, grid and tooltip colors when themes change.

Test theme switching on desktop, tablet and mobile.

---

# 10. PUBLIC WEBSITE PAGES

Create the following pages:

1. Home.
2. About Us.
3. Wedding Venues.
4. Venue Details.
5. Wedding Packages.
6. Package Details.
7. Vendors and Services.
8. Contact Us.
9. Login.
10. Registration.
11. Privacy Policy.
12. Terms and Conditions.

## 10.1 Home Page

### Navigation Bar

Include:

- Peacock logo.
- Home.
- About.
- Venues.
- Packages.
- Services.
- Contact.
- Login.
- Register.
- Theme Toggle.

### Hero Section

Main heading:

"Plan Your Perfect Wedding Reception"

Subtitle:

"Discover beautiful venues, explore wedding packages and organize every detail of your special celebration with Peacock."

Buttons:

- Explore Venues.
- Plan Your Wedding.

Include elegant wedding reception photography.

### Additional Sections

- Featured Venues.
- Popular Wedding Packages.
- Available Wedding Services.
- How Peacock Works.
- Why Choose Peacock.
- Customer Testimonials.
- Contact Information.
- Professional Footer.

Retrieve venue and package information from MySQL.

Never present fabricated statistics or fake testimonials as real customer information.

When no real testimonials exist, display an appropriate empty state or omit the section.

---

# 11. ADMIN DASHBOARD DESIGN

Create a professional Admin Dashboard with responsive sidebar navigation.

Sidebar:

1. Dashboard
2. Users
3. Venues
4. Availability
5. Bookings
6. Packages
7. Vendors
8. Catering
9. Invitation Cards
10. Guests
11. Payments
12. Reports
13. Feedback
14. Notifications
15. Audit Logs
16. Settings
17. Logout

Dashboard Overview:

- Total Customers.
- Total Venues.
- Total Bookings.
- Pending Bookings.
- Confirmed Bookings.
- Total Verified Revenue.
- Outstanding Payments.
- Upcoming Events.

Include:

- Booking status chart.
- Monthly revenue chart.
- Recent booking table.
- Upcoming event list.
- Recent activities.
- Pending approval section.

Use Chart.js with real database data.

Every dashboard statistic must be calculated from actual database records.

---

# 12. CUSTOMER DASHBOARD DESIGN

Create a welcoming and professional Customer Dashboard.

Sidebar:

1. Overview
2. My Profile (Customer name is "Cherry")
3. Browse Venues
4. Wedding Packages
5. My Bookings
6. Vendors
7. Catering
8. My Guests
9. Invitations
10. Seating Planner
11. Budget Tracker
12. Payments
13. Event Schedule
14. Notifications
15. Feedback
16. Logout

Dashboard Overview:

- Wedding overview.
- Upcoming wedding date.
- Selected venue.
- Selected package.
- Booking status.
- Total budget.
- Estimated expenses.
- Remaining budget.
- Guest count.
- Planning progress.
- Recent notifications.

Use real customer-specific database information.

Customers must never see another customer's private dashboard information.

---

# 13. FUNCTIONAL IMPLEMENTATION

Every relevant button, link, form, filter and navigation item must perform its intended action.

Implement:

- Complete CRUD operations.
- Registration and login.
- Role-based authorization.
- Search.
- Filtering.
- Pagination.
- Sorting where appropriate.
- Form validation.
- Image uploading.
- Database operations.
- Booking availability validation.
- Booking approval workflows.
- Budget calculations.
- Payment management.
- Notification generation.
- Report generation.
- CSV exports.
- PDF exports.
- Success messages.
- Error messages.
- Confirmation dialogs.
- Empty states.
- Loading states.

Use server-side validation even when frontend validation exists.

Do not use static hardcoded dashboard values.

Do not leave important modules as placeholder pages.

If an external integration or credential is unavailable, implement a safe local workflow and document the limitation.

---

# 14. SECURITY REQUIREMENTS

Follow professional web application security practices.

## 14.1 Authentication

Implement:

- Secure password hashing using Argon2 or bcrypt.
- Password validation.
- Session expiration.
- HTTP-only authentication cookies.
- Secure logout.
- Login and registration validation.
- Password reset workflow.
- Secure session invalidation.
- Rate limiting for sensitive authentication endpoints.

Never store plain-text passwords.

## 14.2 Authorization

Implement strict RBAC.

- Admin-only route protection.
- Customer-only route protection.
- Customer ownership checks.
- Prevent unauthorized direct object access.
- Protect sensitive administrative operations.
- Never trust role information supplied by the frontend.

## 14.3 Application Security

Implement:

- CSRF protection for cookie-authenticated state-changing requests.
- Server-side input validation.
- SQL injection prevention through parameterized queries and ORM operations.
- XSS protection.
- Secure file uploads.
- File type and file size limits.
- Safe file storage.
- Environment variables for secrets.
- HTTPS in production.
- Appropriate CORS configuration.
- Rate limiting for sensitive endpoints.
- Secure error handling.

## 14.4 Phone Number Encryption

Never store plain-text phone number in database.But it( phone number )show in frontend website page. like 09984122721 or +959981485229.

Important distinction:

Passwords should be securely hashed because they do not need to be recovered.

Phone numbers should be encrypted because authorized application workflows may need to display them again.

## 14.5 Financial Security

- Protect payment records.
- Preserve payment history.
- Require Admin authorization for verification.
- Prevent unauthorized financial changes.
- Maintain audit logs.
- Restrict payment receipt access.
- Never store payment credentials.

Never expose:

- Password hashes.
- Secret keys.
- Database credentials.
- Private customer information.
- Payment receipts to unauthorized users.

---

# 15. NON-FUNCTIONAL REQUIREMENTS

NFR-01: API Performance

Target p95 response latency of 200 milliseconds or less for lightweight database-backed endpoints under documented test conditions.

NFR-02: Page Performance

Target initial page loading within 3 seconds under defined normal conditions.

Aim for LCP within 3 seconds.

Optimize images, CSS, JavaScript, database queries, static assets, template rendering and browser caching.

Use lazy loading where appropriate.

NFR-03: Security

Protect customer and financial information.

NFR-04: Usability

The system must be easy to understand for customers with basic computer skills.

NFR-05: Reliability

Handle errors gracefully and avoid unexpected data loss.

NFR-06: Availability

Remain accessible when the hosting environment is operational.

NFR-07: Scalability

Support increasing numbers of customers, venues and bookings.

NFR-08: Maintainability

Use modular architecture and reusable components.

NFR-09: Compatibility

Support:

- Google Chrome.
- Microsoft Edge.
- Mozilla Firefox.

NFR-10: Responsiveness

Support:

- Desktop.
- Laptop.
- Tablet.
- Mobile phones.

NFR-11: Data Integrity

Maintain accurate database relationships and financial calculations.

NFR-12: Backup and Recovery

Provide database backup and recovery procedures.

NFR-13: Privacy

Only authorized users may access private information.

NFR-14: Error Handling

Display clear validation and error messages.

NFR-15: Accessibility

Use semantic HTML, labels, keyboard navigation and sufficient color contrast.

NFR-16: Theme Accessibility

Both themes must maintain readable text, sufficient contrast and visible keyboard focus indicators.

---

# 16. PROJECT ARCHITECTURE

Use a modular FastAPI architecture.

Recommended structure:

```text
peacock/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── database.py
│   │   ├── permissions.py
│   │   └── encryption.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── venue.py
│   │   ├── package.py
│   │   ├── booking.py
│   │   ├── vendor.py
│   │   ├── guest.py
│   │   ├── payment.py
│   │   ├── invitation.py
│   │   ├── seating.py
│   │   ├── budget.py
│   │   ├── notification.py
│   │   ├── feedback.py
│   │   └── audit_log.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── venue.py
│   │   ├── package.py
│   │   ├── booking.py
│   │   └── payment.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── admin.py
│   │   ├── customer.py
│   │   ├── venues.py
│   │   ├── packages.py
│   │   ├── bookings.py
│   │   ├── vendors.py
│   │   ├── catering.py
│   │   ├── guests.py
│   │   ├── invitations.py
│   │   ├── seating.py
│   │   ├── budgets.py
│   │   ├── payments.py
│   │   ├── schedules.py
│   │   ├── notifications.py
│   │   ├── feedback.py
│   │   └── reports.py
│   │
│   ├── services/
│   │   ├── booking_service.py
│   │   ├── payment_service.py
│   │   ├── budget_service.py
│   │   ├── notification_service.py
│   │   ├── report_service.py
│   │   └── encryption_service.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── public/
│   │   ├── admin/
│   │   ├── customer/
│   │   └── components/
│   │
│   └── static/
│       ├── css/
│       ├── js/
│       ├── images/
│       └── icons/
│
├── alembic/
├── tests/
├── media/
│   ├── venues/
│   ├── packages/
│   ├── vendors/
│   ├── invitations/
│   └── payment_receipts/
│
├── scripts/
│
├── docs/
│
├── requirements.txt
├── .env.example
├── .gitignore
├── alembic.ini
├── README.md
└── run.py
```

Adjust the architecture when technically necessary while preserving modularity and separation of concerns.

Do not put all models, routes and business logic in one Python file.

Keep business logic in service modules and HTTP handling in routers.

---

# 17. DEVELOPMENT WORKFLOW

Follow these stages in order.

## STAGE 1: WORKSPACE INSPECTION

Before writing code:

1. Inspect the entire existing workspace.
2. Identify existing files and folders.
3. Identify installed dependencies.
4. Identify existing database configuration.
5. Identify existing frontend and backend code.
6. Identify incomplete or broken functionality.
7. Identify existing reusable components.
8. Identify available images and design references.
9. Determine what should be preserved, modified or created.

Do not delete existing working code without a clear reason.

**Deliverable:** Workspace Inspection Summary.

## STAGE 2: PROJECT PLANNING

Create:

- Project development plan.
- Functional requirements checklist.
- Non-functional requirements checklist.
- User role and permission matrix.
- Application architecture.
- Database entity relationship design.
- Page navigation structure.
- Module dependency plan.
- Development milestones.

**Deliverable:** Complete Technical Development Plan.

## STAGE 3: DATABASE DESIGN

1. Design normalized MySQL tables.
2. Define primary and foreign keys.
3. Define relationships.
4. Define constraints.
5. Define indexes.
6. Create SQLAlchemy models.
7. Configure database connection.
8. Configure Alembic.
9. Create initial migrations.
10. Test database connectivity.

**Deliverables:**

- Database schema.
- ER diagram.
- SQLAlchemy models.
- Alembic migrations.

## STAGE 4: BACKEND DEVELOPMENT

Implement:

1. Configuration.
2. Database connection.
3. Authentication.
4. Authorization.
5. User management.
6. Venue management.
7. Availability management.
8. Package management.
9. Booking management.
10. Vendor management.
11. Catering management.
12. Guest management.
13. Invitations.
14. Seating arrangements.
15. Budget management.
16. Payment management.
17. Event scheduling.
18. Notifications.
19. Feedback.
20. Reports.
21. Audit logs.

Implement business logic in service modules.

Use routers for HTTP endpoints.

Validate requests with Pydantic.

**Deliverable:** Functional backend connected to MySQL.

## STAGE 5: FRONTEND DEVELOPMENT

Develop:

- Public website.
- Login page.
- Registration page.
- Admin dashboard.
- Customer dashboard.
- All management pages.
- Responsive navigation.
- Reusable components.
- Tables and forms.
- Charts.
- Calendar interfaces.
- Confirmation dialogs.
- Notifications.
- Empty and error states.

Use Jinja2 templates and Bootstrap 5.

Create a consistent premium Peacock design.

**Deliverable:** Complete responsive frontend connected to backend routes.

## STAGE 6: THEME IMPLEMENTATION

Implement:

- Light Mode.
- Dark Mode.
- Theme toggle.
- Theme persistence.
- CSS theme variables.
- Theme-aware Chart.js charts.
- Responsive theme controls.

Test all public, admin and customer pages in both themes.

**Deliverable:** Fully functional application-wide theme switching.

## STAGE 7: MODULE INTEGRATION

Connect all frontend modules to actual backend endpoints.

Verify:

- CRUD operations.
- Database persistence.
- Authentication.
- Authorization.
- Ownership checks.
- Booking workflows.
- Payment workflows.
- Budget calculations.
- Guest management.
- Seating assignments.
- Invitations.
- Notifications.
- Reports.

No important feature should remain a decorative interface.

**Deliverable:** Integrated Full-Stack Application.

## STAGE 8: TESTING AND DEBUGGING

Use Pytest for backend testing.

Test:

- Registration.
- Login.
- Logout.
- Password hashing.
- Session expiration.
- Admin permissions.
- Customer permissions.
- Customer data isolation.
- Venue CRUD.
- Package CRUD.
- Booking creation.
- Booking approval.
- Booking rejection.
- Booking cancellation.
- Venue conflict prevention.
- Guest CRUD.
- RSVP updates.
- Seating capacity validation.
- Budget calculations.
- Payment submission.
- Payment verification.
- Notification generation.
- Feedback restrictions.
- Report generation.
- Invitation management.
- Image upload validation.
- Phone number encryption and decryption.
- Light and dark theme switching.

Also perform:

- Integration testing.
- Database testing.
- Form validation testing.
- Responsive UI testing.
- Security testing.
- Browser compatibility testing.

Fix errors before proceeding.

Do not report tests as passed unless they actually run successfully.

## STAGE 9: PERFORMANCE OPTIMIZATION

Optimize:

- SQL queries.
- Database indexes.
- Image sizes.
- Static assets.
- CSS.
- JavaScript.
- Template rendering.
- API response times.

Measure performance using appropriate tools.

Document actual results rather than inventing performance figures.

## STAGE 10: DOCUMENTATION

Create complete project documentation.

Required documents:

1. PROJECT_OVERVIEW.md
2. REQUIREMENTS.md
3. USER_ROLES_AND_PERMISSIONS.md
4. SYSTEM_ARCHITECTURE.md
5. DATABASE_DESIGN.md
6. ER_DIAGRAM.md
7. USE_CASE_DIAGRAM.md
8. ACTIVITY_DIAGRAMS.md
9. SEQUENCE_DIAGRAMS.md
10. API_DOCUMENTATION.md
11. INSTALLATION_GUIDE.md
12. CONFIGURATION_GUIDE.md
13. USER_MANUAL.md
14. ADMIN_MANUAL.md
15. TESTING_REPORT.md
16. SECURITY_DOCUMENTATION.md
17. KNOWN_LIMITATIONS.md
18. FUTURE_ENHANCEMENTS.md

Documentation must describe the actual implemented application.

Do not document features that do not exist.
_Everything You Did should be recorded under/docs/,that should include summary of the last thing you did as a context,Summary of every phase should be recorded as well.

## STAGE 11: FINAL VERIFICATION

Before declaring the project complete:

1. Verify all required files exist.
2. Verify MySQL connection.
3. Verify Alembic migrations.
4. Verify application startup.
5. Verify all routes.
6. Verify authentication and authorization.
7. Verify all CRUD operations.
8. Verify all major workflows.
9. Verify database persistence.
10. Verify both themes.
11. Verify responsive layouts.
12. Verify security checks.
13. Run automated tests.
14. Fix remaining errors.
15. Update documentation.
16. Provide a final development report.

**Deliverable:** Tested and Documented Peacock Application.

---

# 18. APPLICATION STARTUP AND SETUP

Provide a simple and reliable local development setup.

Creating a virtual environment:

```bash
python -m venv venv
```

Activating on Windows:

```bash
venv\Scripts\activate
```

Installing dependencies:

```bash
pip install -r requirements.txt
```

Configure the environment file:

```bash
.env
```

Create the MySQL database.

Run database migrations:

```bash
alembic upgrade head
```

Start the application:

```bash
uvicorn app.main:app --reload
```

Provide the local application URL:

```text
http://127.0.0.1:8000
```

Ensure setup instructions match the actual project structure.

Never expose `.env` secrets in GitHub.

Include a `.env.example` with safe placeholder values.

Provide a database initialization procedure and a secure method for creating the first Admin account.

Never create a publicly accessible default Admin password.

---

# 19. DEVELOPMENT RULES FOR THE AGENT

Follow these rules throughout development.

1. Work directly in the existing workspace.
2. Inspect before modifying.
3. Follow the defined architecture.
4. Use modular source code.
5. Avoid unnecessary dependencies.
6. Avoid duplicate functionality.
7. Avoid hardcoded dashboard statistics.
8. Avoid fake payment verification.
9. Avoid fake customer testimonials.
10. Avoid placeholder pages for required modules.
11. Use reusable frontend components.
12. Use reusable backend services.
13. Maintain database consistency.
14. Implement server-side authorization.
15. Validate all user inputs.
16. Handle exceptions appropriately.
17. Write meaningful comments where needed.
18. Maintain consistent naming conventions.
19. Test each module after implementation.
20. Fix errors before proceeding.
21. Update documentation when architecture or functionality changes.
22. Preserve working functionality.
23. Never claim untested functionality is complete.
24. Never expose private information or credentials.
25. Do not silently remove existing functionality.
26. Do not use fabricated database records as real business data.
27. Use clearly labelled development seed data when necessary.
28. Use database transactions for critical operations.
29. Maintain an updated progress checklist.
30. Do not skip development stages.

---

# 20. FINAL ACCEPTANCE CRITERIA

The application will be considered complete only when the following requirements are satisfied.

## Frontend

- Professional Peacock branding.
- Elegant public website.
- Functional navigation.
- Responsive layouts.
- Admin dashboard.
- Customer dashboard.
- Complete management interfaces.
- Light Mode.
- Dark Mode.
- Theme persistence.

## Backend

- FastAPI application.
- Modular routers.
- Modular services.
- Secure authentication.
- Role-based authorization.
- Complete CRUD operations.
- Validated business workflows.

## Database

- MySQL integration.
- Normalized schema.
- SQLAlchemy models.
- Alembic migrations.
- Foreign key relationships.
- Financial data integrity.
- Database transactions.

## Functionality

- Venue browsing.
- Package selection.
- Booking management.
- Booking approval.
- Vendor selection.
- Catering management.
- Guest management.
- Digital invitations.
- Seating arrangements.
- Budget tracking.
- Payment submission.
- Payment verification.
- Event scheduling.
- Notifications.
- Feedback.
- Reports.

## Security

- Password hashing.
- Session security.
- CSRF protection.
- RBAC.
- Ownership checks.
- Phone number encryption.
- Secure file uploads.
- Audit logs.
- Protected payment information.

## Quality

- Application runs successfully.
- Database operations work.
- Important workflows pass tests.
- No unresolved critical errors.
- Documentation is complete.
- Setup instructions are verified.

---

# 21. FINAL AGENT INSTRUCTIONS

Begin with:

**STAGE 1: WORKSPACE INSPECTION.**

Do not immediately generate the entire application in one enormous code-writing operation.

Work progressively through each development stage.

After each stage:

1. Summarize completed work.
2. Identify files created or modified.
3. Run relevant checks.
4. Identify remaining issues.
5. Fix errors.
6. Update the development checklist.
7. Proceed to the next stage.

Maintain a project progress checklist so that no required module is forgotten.

Prioritize:

1. Functional correctness.
2. Security.
3. Database integrity.
4. Business logic.
5. Usability.
6. Responsive design.
7. Visual quality.
8. Performance.
9. Documentation.

If an essential requirement is ambiguous, make a reasonable engineering decision and document the assumption.

If credentials or external integrations are unavailable, implement a safe alternative and clearly document the limitation.

**MOST IMPORTANT:**

Build PEACOCK as a complete working web application, not a visual demonstration.

Every important button must work. Every form must submit correctly. Every major module must connect to the backend. Every database operation must persist correctly. Every user must only access information permitted by their role.

Do not declare the project finished until the final verification stage has been completed.

**Start by inspecting the existing workspace and presenting the Stage 1 inspection report. Do not overwrite existing project files before understanding them.**