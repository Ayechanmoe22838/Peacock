# FUTURE ENHANCEMENTS
# PEACOCK – Smart Wedding Reception Management System

---

## 1. Roadmap & Strategic Extensions

The modular, service-oriented architecture of PEACOCK provides a foundation for extending platform capabilities in subsequent release cycles.

---

## 2. Planned Functional & Architectural Upgrades

### 2.1 Automated KBZPay & WavePay Merchant Direct API Integration
- **Objective:** Transition from human-verified payment slips to instant QR payment verification via direct KBZPay Partner API and WavePay B2B Gateway.
- **Components:**
  - Automated dynamic QR code generation (KBZPay PWA / Mini-Program QR).
  - Webhook listener with HMAC-SHA256 signature verification.
  - Instant booking confirmation upon verified bank webhook callback.

### 2.2 Interactive 2D/3D Banquet Hall Seating Drag-and-Drop Floorplanner
- **Objective:** Upgrade the current table-and-seat list builder to an interactive visual drag-and-drop floorplan designer.
- **Components:**
  - HTML5 Canvas / Fabric.js or Three.js interactive canvas.
  - Spatial hall layout customization: stage position, dance floor, bridal catwalk, VIP round tables, buffet island, and audiovisual booths.
  - Real-time guest card dragging between tables with capacity clamping.

### 2.3 Automated Print-Ready PDF Wedding Invitation Generation
- **Objective:** Allow couples to download high-resolution CMYK 300 DPI vector PDF stationery cards for physical printing at commercial print shops.
- **Components:**
  - ReportLab PDF generator with custom Burmese/Pyidaungsu font embedding.
  - Golden foil stamp overlay guides and print bleed markers.

### 2.4 Multi-Language Localization (Burmese & English)
- **Objective:** Provide a bilingual interface toggle between Burmese (Zawgyi / Unicode) and English.
- **Components:**
  - Gettext / Babel internationalization (`i18n`) integration with Jinja2.
  - Language selection dropdown in navigation with localStorage preference persistence.

### 2.5 Real-Time WebSocket Notifications & Live Chat
- **Objective:** Enable instant two-way messaging between wedding couples and venue administrators during reception planning.
- **Components:**
  - FastAPI WebSocket endpoint (`/ws/chat/{booking_id}`).
  - Redis Pub/Sub for horizontal scaling across worker processes.
  - Read receipts and typing indicators.

### 2.6 Mobile Push Notifications (PWA Support)
- **Objective:** Progressive Web App (PWA) manifest and Service Worker for mobile notification delivery on Android and iOS devices.
- **Components:**
  - Web Push API integration with VAPID keys.
  - Offline venue browsing with cache storage.
