# Additional Implementation Plan: Advanced Request Sourcing Features

**Goal:** Implement points 6 to 10 of the design spec (Certifications, Supply Chain, Ranking, Contracts).

## 1. Certifications & Compliance (Point 7)
**Goal:** Allow Request to require specific certs and Sellers to upload proofs.

### Backend
- [MODIFY] `SourcingRequest` model: Add `required_certs` (JSON List).
- [MODIFY] `SourcingOffer` model: Add `cert_proofs_urls` (JSON List).
- [MODIFY] API: Validate that if Request has `required_certs`, Offer MUST have `cert_proofs_urls` not empty.

### Frontend
- [MODIFY] `CreateRequestPage`: Add multi-select for "Required Certs" (Organic, Fairtrade).
- [MODIFY] `OfferCreation` (Not yet built, implied): Allow file upload for certs.

## 2. Supply Chain & Logistics (Point 8)
**Goal:** Track post-deal progress (FOB).

### Backend
- [MODIFY] `SourcingRequest` model: Add `logistics_status` (Enum: PREPARING, TRANSIT_TO_PORT, AT_PORT, FOB_COMPLETE).
- [NEW] Endpoint `PUT /requests/{id}/logistics`: Update status (Admin/Seller).

### Frontend
- [MODIFY] `RequestDetailPage`: Add a visual "Supply Chain Tracker" step-bar below the Mega-Bar.

## 3. Producer Ranking "Airbnb-Like" (Point 9)
**Goal:** Sort offers by Trust Score.

### Backend
- [MOCK] Creating a `User` table or mock service that returns a `trust_score` for each Facilitator.
- [MODIFY] `GET /requests/{id}`: In the `offers` list, sort by `trust_score` DESC by default.

## 4. Contract Generation (Point 10)
**Goal:** Generate a PDF Contract.

### Backend
- [NEW] Service `app/services/pdf_service.py`: Use `reportlab` to generate a PDF.
- [NEW] Endpoint `POST /requests/{id}/contract`: Generates PDF, uploads to S3 (mocked), returns URL.

### Frontend
- [MODIFY] `RequestDetailPage`: Add "Generate Contract" button when coverage > 0%.
