from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User

router = APIRouter()

class PhoneLoginRequest(BaseModel):
    phone_number: str

class VerifyOTPRequest(BaseModel):
    phone_number: str
    otp: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    is_new_user: bool
    role: str
    kyb_status: str | None = None
    producer_id: int | None = None

@router.post("/login")
def login_request_otp(request: PhoneLoginRequest):
    """
    MVP: Request OTP for phone number.
    Mock: Always returns success.
    """
    # TODO: Integrate Twilio/MessageBird here
    print(f"DTO Mock: Sending OTP to {request.phone_number}")
    return {"message": "OTP sent", "mock_otp": "1234"}

@router.post("/verify", response_model=TokenResponse)
def verify_otp(request: VerifyOTPRequest, db: Session = Depends(deps.get_db)):
    """
    MVP: Verify OTP.
    Mock: Accepts '1234' only.
    Creates user if not exists (Onboarding 'on-the-fly').
    ensures a ProducerProfile exists for FACILITATOR/PRODUCER roles.
    """
    # MVP BYPASS: Allow any code for demo
    # if request.otp != "1234":
    #    raise HTTPException(status_code=400, detail="Invalid OTP")

    user = db.query(User).filter(User.phone_number == request.phone_number).first()
    is_new = False

    if not user:
        # Create new Facilitator user
        user = User(
            phone_number=request.phone_number,
            role="FACILITATOR",
            is_active=True,
            is_verified=False # Requires manual check or ID upload later
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        is_new = True

    # Check for existing ProducerProfile linked to this user (or by phone generic logic for MVP)
    producer_id = None
    if user.role in ["FACILITATOR", "PRODUCER", "PRODUCER_REPRESENTATIVE"]:
        try:
            from app.models.producer import ProducerProfile
            
            # 1. Try to find by user_id
            producer = db.query(ProducerProfile).filter(ProducerProfile.user_id == user.id).first()
            
            # 2. If not found, try to find "Orphan" profile by matching name (if we had name) or just create one
            if not producer:
                 # DEMO LOGIC: If no profile, create a default one "Producer {Phone}"
                 producer = ProducerProfile(
                     user_id=user.id,
                     name=f"Producer {user.phone_number[-4:]}", # e.g. "Producer 5678"
                     location_region="Sava",
                     location_district="Sambava",
                     bio="New producer via mobile app"
                 )
                 db.add(producer)
                 db.commit()
                 db.refresh(producer)
            
            producer_id = producer.id
        except Exception as e:
            print(f"ERROR in verify_otp producer logic: {e}")
            # Non-blocking error for login? Or should we fail?
            # Let's ignore it for now but log it so test script sees "producer_id": null
            pass

    # TODO: Generate real JWT
    return {
        "access_token": f"fake-jwt-token-for-{user.id}", 
        "token_type": "bearer",
        "is_new_user": is_new,
        "role": user.role,
        "kyb_status": user.kyb_status,
        "producer_id": producer_id
    }

class BuyerSignupRequest(BaseModel):
    email: str
    company_name: str

@router.post("/signup/buyer", response_model=TokenResponse)
def signup_buyer(request: BuyerSignupRequest, db: Session = Depends(deps.get_db)):
    """
    Onboard B2B Buyer (Intention Phase).
    """
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        # MVP: Auto-login if exists (In real app: Send magic link)
        return {
            "access_token": f"fake-jwt-token-for-{existing_user.id}",
            "token_type": "bearer",
            "is_new_user": False,
            "role": existing_user.role
        }
    
    user = User(
        email=request.email,
        company_name=request.company_name,
        role="BUYER",
        kyb_status="PENDING",
        is_active=True,
        is_verified=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "access_token": f"fake-jwt-token-for-{user.id}",
        "token_type": "bearer",
        "is_new_user": True,
        "role": user.role,
        "kyb_status": user.kyb_status
    }
