# Implementation Plan: Request Sourcing Module

**Date:** 2026-01-10
**Goal:** Implement the Request Sourcing / RFP module backend.

## Proposed Changes

### Database Layer (SQLAlchemy Models)

#### [NEW] `backend/app/models/sourcing.py`
- Create `SourcingRequest` model:
    - `id`, `buyer_id`, `product_type`, `volume_target_kg`, `price_target_usd`, `grade_target`.
    - `specs_json` (for dynamic criteria).
    - `accepts_partial` (bool).
    - `status` (OPEN, CLOSED, FULFILLED).
- Create `SourcingOffer` model:
    - `id`, `request_id`, `facilitator_id`.
    - `volume_offered_kg`, `price_offered_usd`.
    - `status` (PENDING, ACCEPTED, REJECTED, NEGOTIATING).
    - `photos_json`.

### Schema Layer (Pydantic)

#### [NEW] `backend/app/schemas/sourcing.py`
- `SourcingRequestCreate` / `SourcingRequestResponse`
- `SourcingOfferCreate` / `SourcingOfferResponse`

### API Layer

#### [NEW] `backend/app/api/v1/endpoints/sourcing.py`
- `POST /requests/` -> Create Request
- `GET /requests/` -> List Requests (Filterable)
- `GET /requests/{id}` -> Detail with progress bar stats
- `POST /requests/{id}/offers` -> Submit Offer
- `PUT /offers/{id}` -> Update status (Accept/Negotiate)

#### [MODIFY] `backend/app/api/v1/api.py`
- Include the new router `sourcing`.

## Verification Plan

### Automated Tests
- Since there are no existing tests visible, I will rely on manual testing instructions or creating a simple test script if possible.
- Ideally, I would use `pytest` to test the endpoints.

### Manual Verification
- Start the server.
- Use Swagger UI (`/docs`) to:
    1. Create a Request.
    2. Create 2 Offers for this request.
    3. Check the Detail view to see the aggregated coverage.
