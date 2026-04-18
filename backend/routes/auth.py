from fastapi import APIRouter
from pydantic import BaseModel
from auth.auth_handler import signup, login, mark_email_verified
import random
from services.email_service import send_otp_email

router = APIRouter()

otp_store = {}


class AuthRequest(BaseModel):
    name: str | None = None
    email: str
    password: str


class OTPRequest(BaseModel):
    email: str
    otp: str


# SEND OTP
@router.post("/send-otp")
def send_otp(req: dict):
    email = req.get("email")

    if not email or "@" not in email:
        return {"success": False}

    otp = str(random.randint(100000, 999999))
    otp_store[email] = otp

    # SEND REAL EMAIL
    send_otp_email(email, otp)

    return {"success": True}


# VERIFY OTP
@router.post("/verify-otp")
def verify_otp(req: OTPRequest):

    email = req.email
    user_otp = req.otp

    real_otp = otp_store.get(email)

    if not real_otp:
        return {"success": False, "message": "OTP expired or not sent"}

    if user_otp != real_otp:
        return {"success": False, "message": "Invalid OTP"}

    mark_email_verified(email)
    otp_store.pop(email, None)

    return {"success": True, "message": "Email verified"}


# SIGNUP
@router.post("/signup")
def signup_api(req: AuthRequest):
    success, msg = signup(req.name, req.email, req.password)
    return {"success": success, "message": msg}


# LOGIN
@router.post("/login")
def login_api(req: AuthRequest):
    success, msg = login(req.email, req.password)
    return {"success": success, "message": msg}