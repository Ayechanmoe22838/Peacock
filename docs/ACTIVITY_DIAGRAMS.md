# ACTIVITY DIAGRAMS
# PEACOCK – Smart Wedding Reception Management System

---

## 1. Booking Workflow Activity Diagram

This activity diagram illustrates the multi-stage lifecycle of a wedding reception reservation, from customer venue selection to conflict validation, admin review, and confirmation.

```mermaid
flowchart TD
    Start([Customer initiates booking]) --> SelectVenue[Select Venue, Date, Time & Package]
    SelectVenue --> CheckAvailability{Is Venue Available & Not Blacked Out?}
    
    CheckAvailability -- No --> ShowConflict[Display Conflict Error & Suggest Alternative Dates]
    ShowConflict --> SelectVenue
    
    CheckAvailability -- Yes --> EnterDetails[Input Guest Count & Special Requests]
    EnterDetails --> ServerCalc[Server calculates Venue + Package + Service Costs]
    ServerCalc --> SubmitRequest[Customer submits Booking Request]
    
    SubmitRequest --> StatusPending[Status set to 'Pending']
    StatusPending --> NotifyAdmin[System notifies Administrator]
    
    NotifyAdmin --> AdminReview{Admin Reviews Booking}
    AdminReview -- Rejected --> InputReason[Admin provides Rejection Reason]
    InputReason --> StatusRejected[Status set to 'Rejected']
    StatusRejected --> NotifyCustomerReject[Notify Customer of Rejection]
    NotifyCustomerReject --> EndBooking([Booking Concluded])
    
    AdminReview -- Approved --> StatusApproved[Status set to 'Approved']
    StatusApproved --> NotifyCustomerApprove[Notify Customer to Submit Deposit]
    
    NotifyCustomerApprove --> CustomerPays[Customer transfers Deposit via KBZPay]
    CustomerPays --> SubmitProof[Submit KPay Reference & Screenshot Slip]
    SubmitProof --> VerifyPayment[Admin verifies Transaction]
    
    VerifyPayment -- Approved --> StatusConfirmed[Status updated to 'Confirmed']
    StatusConfirmed --> LockCalendar[Date & Time Permanently Locked in Calendar]
    LockCalendar --> EndSuccess([Wedding Confirmed])
```

---

## 2. KBZPay Manual Payment Verification Activity Diagram

This diagram details the financial reconciliation workflow ensuring zero automated fabricated payments and strict human administrative oversight.

```mermaid
flowchart TD
    PStart([Customer accesses Payments Page]) --> CheckBalance[System displays verified paid & balance amount]
    CheckBalance --> ViewInstructions[Customer views official Peacock KPay Merchant Details]
    ViewInstructions --> KPayTransfer[Customer executes transfer in KBZPay mobile app]
    
    KPayTransfer --> EnterRef[Customer enters 16-digit Transaction Reference]
    EnterRef --> UploadSlip[Upload transaction screenshot receipt]
    UploadSlip --> SubmitRecord[Submit Payment for Verification]
    
    SubmitRecord --> StatusPendingVerif[Payment created with status 'Pending Verification']
    StatusPendingVerif --> AdminInbox[Receipt appears on Admin Verification Queue]
    
    AdminInbox --> InspectReceipt{Admin checks KBZPay Merchant Account}
    
    InspectReceipt -- Mismatch / Invalid --> EnterAdminNotes[Admin notes rejection reason]
    EnterAdminNotes --> SetRejected[Payment status set to 'Rejected']
    SetRejected --> NotifyCustomerFailure[Customer alerted with admin feedback]
    NotifyCustomerFailure --> KPayTransfer
    
    InspectReceipt -- Validated & Received --> AdminApprove[Admin clicks 'Approve Payment']
    AdminApprove --> CreditLedger[System updates paid_amount and decrements balance_amount]
    CreditLedger --> UpdateBookingStatus{Is deposit threshold met?}
    
    UpdateBookingStatus -- Yes --> PromoteConfirmed[Booking status updated to 'Confirmed']
    UpdateBookingStatus -- Fully Paid --> ZeroBalance[Balance cleared to 0 MMK]
    
    ZeroBalance --> CreateAuditLog[Immutable Audit Log written with Admin ID & Timestamp]
    PromoteConfirmed --> CreateAuditLog
    CreateAuditLog --> NotifyCustomerSuccess[Customer receives Payment Verification Alert]
    NotifyCustomerSuccess --> PEnd([Payment Settled])
```

---

## 3. Digital Invitation & Guest RSVP Activity Diagram

```mermaid
flowchart TD
    IStart([Customer opens Invitation Studio]) --> PickTemplate[Select 1 of 13 Stationery Designs]
    PickTemplate --> EnterWeddingDetails[Set Couple Names, Wedding Date, Venue & Message]
    EnterWeddingDetails --> LivePreview[System renders real-time interactive preview]
    LivePreview --> SaveInvitation[Save Invitation & Generate Unique Token]
    
    SaveInvitation --> GetLink[Generate shareable URL: /invitation/token]
    GetLink --> ShareGuests[Couple shares link via SMS, Viber, Telegram or Social Media]
    
    ShareGuests --> GuestVisits[Guest opens public invitation link]
    GuestVisits --> IncrementViews[System increments page views count]
    IncrementViews --> DisplayCard[Display high-resolution card & event details]
    
    DisplayCard --> GuestRSVP{Will Guest Attend?}
    GuestRSVP -- Yes --> EnterRSVPYes[Input Name, Phone, Plus-Ones & Dietary Preferences]
    GuestRSVP -- No --> EnterRSVPNo[Input Name & Regret Message]
    
    EnterRSVPYes --> SaveGuestDB[Save guest entry into database with status 'Accepted']
    EnterRSVPNo --> SaveGuestDB2[Save guest entry with status 'Declined']
    
    SaveGuestDB --> RefreshStats[Real-time RSVP statistics updated on Customer Dashboard]
    SaveGuestDB2 --> RefreshStats
    RefreshStats --> IEnd([RSVP Complete])
```
