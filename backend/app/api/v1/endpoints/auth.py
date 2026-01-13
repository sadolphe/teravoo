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
    """
    if request.otp != "1234":
        raise HTTPException(status_code=400, detail="Invalid OTP")

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

    # TODO: Generate real JWT
    return {
        "access_token": f"fake-jwt-token-for-{user.id}", 
        "token_type": "bearer",
        "is_new_user": is_new,
        "role": user.role,
        "kyb_status": user.kyb_status
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
