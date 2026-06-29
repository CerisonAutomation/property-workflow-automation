# n8n Workflows

Production n8n workflow exports for Christiano Property Management Malta.

## Malta Eco Tax — `malta-eco-tax-workflow.json`

Automates Malta eco contribution collection for Guesty/Airbnb reservations.

### Flow

```
Guesty Webhook
  → Normalize Reservation (field mapping + tax calc)
  → Guard (skip cancelled / no email / zero tax)
    ├─ [valid]   → Log to Google Sheets
    │             → Create Stripe Payment Link
    │             → Merge Data
    │             → Email Guest (Gmail)
    │             → Update Sheet (link_sent)
    │             → Done Summary
    └─ [invalid] → Log Skip
```

### Tax formula

```
ecoTax = guestsCount × nights × €0.50
```

### Setup checklist

- [ ] Import `malta-eco-tax-workflow.json` into n8n (Settings → Import)
- [ ] Replace `REPLACE_WITH_GOOGLE_SHEET_ID` in both Google Sheets nodes
- [ ] Create sheet named `EcoTaxLog` with columns: `Timestamp, ReservationID, ListingName, GuestName, GuestEmail, CheckIn, CheckOut, Nights, Guests, EcoTax_EUR, PaymentStatus, StripeLink, EmailSentAt`
- [ ] Connect Gmail credential (or swap Gmail node for SMTP/Resend)
- [ ] Add `STRIPE_SECRET_KEY` to n8n environment variables
- [ ] Copy webhook URL from `Guesty Reservation Webhook` node → paste into Guesty Dashboard → Webhooks → `reservation.created` + `reservation.updated`
- [ ] Activate the workflow

### Production notes

- Stripe `after_completion.redirect.url` defaults to `https://christianopropertymanagement.com/thank-you` — update if needed
- `replyTo` defaults to `info@christianopropertymanagement.com` — update if needed
- Uses total `guestsCount`. To charge only guests over 18, add a pre-arrival form step — Airbnb does not expose guest ages
- For full reconciliation, build a second workflow triggered by `payment_link.completed` Stripe webhook that updates `PaymentStatus → paid` in the sheet
- If Guesty webhook payload differs, adjust field paths in the `Normalize Reservation` node
