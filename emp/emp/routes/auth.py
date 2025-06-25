from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from emp import database, schemas
from emp.hashing import Hash
from emp.jwt_token import create_access_token
from emp.models import user as user_model
from emp.models.password_reset_otp import PasswordResetOTP
from emp.utils.email_utils import send_email
from datetime import datetime, timedelta
import random

router = APIRouter(prefix="", tags=["Authentication"])


@router.post("/login")
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    allowed_domain = "@gmail.com"
    email_lower = request.email.lower()

    if not email_lower.endswith(allowed_domain):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "code": 403,
                "message": f"Email domain must be {allowed_domain}",
                "details": None
            }
        )

    user = db.query(user_model.User).filter(user_model.User.email == email_lower).first()

    if not user:
        return JSONResponse(
            status_code=404,
            content={
                "code": 404,
                "message": "User not found",
                "details": None
            }
        )

    if not Hash.verify(user.password, request.password):
        return JSONResponse(
            status_code=401,
            content={
                "code": 401,
                "message": "Incorrect password",
                "details": None
            }
        )

    if user.role.lower() != request.role.lower():
        return JSONResponse(
            status_code=403,
            content={
                "code": 403,
                "message": "Role mismatch",
                "details": None
            }
        )

    # ✅ Create JWT Token
    access_token = create_access_token(data={"sub": user.email, "role": user.role})

    return JSONResponse(
        status_code=200,
        content={
            "code": 200,
            "message": "Login successful",
            "details": {
                "id": user.custom_id,
                "email": user.email,
                "role": user.role,
                "access_token": access_token,
                "token_type": "bearer"
            }
        }
    )


@router.post("/forgot-password")
async def forgot_password(request: schemas.ForgotPassword, db: Session = Depends(database.get_db)):
    user = db.query(user_model.User).filter(user_model.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate a 6-digit OTP
    otp = str(random.randint(100000, 999999))
    expiry = datetime.utcnow() + timedelta(minutes=5)

    # Remove previous OTPs for this user
    db.query(PasswordResetOTP).filter(PasswordResetOTP.user_id == user.id).delete()

    # Store new OTP
    otp_entry = PasswordResetOTP(user_id=user.id, otp=otp, expires_at=expiry)
    db.add(otp_entry)
    db.commit()

    # Send OTP via email
    subject = "Your OTP for Password Reset"
    body = f"Hi {user.name},\n\nYour OTP for password reset is: {otp}\nIt expires in 5 minutes.\n\nRegards,\nSupport Team"
    await send_email(to_email=user.email, subject=subject, body=body)

    return {"message": "OTP sent to your email"}


@router.post("/reset-password")
def reset_password(request: schemas.ResetPassword, db: Session = Depends(database.get_db)):
    otp_entry = db.query(PasswordResetOTP).filter(
        PasswordResetOTP.otp == request.otp
    ).first()

    if not otp_entry or otp_entry.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    user = db.query(user_model.User).filter(user_model.User.id == otp_entry.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Hash and update new password
    user.password = Hash.bcrypt(request.new_password)
    db.delete(otp_entry)
    db.commit()

    return {"message": "Password updated successfully"}
