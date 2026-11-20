# KNOWN LIMITATIONS
# PEACOCK – Smart Wedding Reception Management System

---

## 1. Overview

In adherence to Section 13 and Section 7 of `implementation.md`:
> *"Do not invent KPay APIs. Do not pretend payments are automatically verified. Only implement automatic verification when authorized API documentation and credentials are available... If an external integration or credential is unavailable, implement a safe local workflow and document the limitation."*

This document provides a transparent, truthful assessment of the current system boundaries and safe fallback workflows.

---

## 2. Identified System Boundaries & Fallback Implementations

### 2.1 KBZPay Payment Verification
- **Limitation:** Direct KBZPay Open Banking API integration requires official business merchant contracts, mutual TLS certificates, corporate partner credentials, and IP whitelisting with KBZ Bank.
- **Implemented Solution:** A human-in-the-loop manual payment verification pipeline is implemented. The customer transfers funds via their official KBZPay mobile app, enters their 16-digit transaction reference number, and uploads the screenshot receipt. Administrators review the transaction reference and slip against their merchant statement and manually verify or reject the payment. This eliminates security vulnerabilities from unauthenticated mock webhooks.

### 2.2 SMS Gateway & Cellular Notifications
- **Limitation:** Direct cellular SMS dispatching (via MPT, Telenor/ATOM, Ooredoo, or Mytel telecommunication gateways) requires localized Myanmar SMS aggregator SMPP credentials.
- **Implemented Solution:** An in-app notification center is fully operational. Customers and administrators receive persistent real-time notifications in their dashboard for booking approvals, rejections, payment status updates, and system alerts.

### 2.3 Automated Image Generation (Canvas to Image Export)
- **Limitation:** Complex server-side rasterization of user-edited fonts and custom HTML5 canvas to high-DPI print files requires heavy headless Chrome/Puppeteer browser binaries.
- **Implemented Solution:** Digital wedding invitations utilize a robust template-driven architecture with 13 stationery card templates extracted from authentic wedding designs. Invitations generate shareable public links (`/invitation/{token}`) with responsive mobile rendering, real-time page-view tracking, and live RSVP capture.

### 2.4 Timezone Considerations
- **Limitation:** All event times and database timestamps are calculated and stored in Myanmar Standard Time (MMT, UTC+06:30). Cross-timezone bookings from overseas diaspora users are converted to Yangon local time for banquet hall scheduling.
