from datetime import datetime
import os
from typing import List
from fastapi import HTTPException, APIRouter
import fastapi as _fastapi
import schemas as _schemas
from utils.email_service import send_email
import sqlalchemy.orm as _orm
import service as _services
import logging
import utils.database as _database
from starlette.responses import RedirectResponse
import json



router = APIRouter()

@router.get("/")
def main():
    return RedirectResponse(url="/docs/")

@router.get("/check_api")
async def check_api():
    return {"status": "Connected to API Successfully"}


# Endpoint to check if the API is live
@router.post("/users" ,  tags = ['User Auth'])
async def create_user(
    user: _schemas.UserCreate, 
    db: _orm.Session = _fastapi.Depends(_database.get_db)):
    db_user = await _services.get_user_by_email(email=user.email, db=db)

    if db_user:
        logging.info('User with that email already exists')
        raise _fastapi.HTTPException(
            status_code=200,
            detail="User with that email already exists")

    user = await _services.create_user(user=user, db=db)
    # success = send_email(
    #     recipient=user.email, 
    #     subject="User account activation", 
    #     body="Your RECIPE user account has been created successfully\nPlease login to activate your account."
    # )
    return _fastapi.HTTPException(
            status_code=201,
            detail="User Registered, Please verify email to activate account !")


@router.post("/auth/token" ,tags = ['User Auth'])
async def generate_token(
    # form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(), 
    user_data: _schemas.GenerateUserToken,
    db: _orm.Session = _fastapi.Depends(_database.get_db)):
    print("Login data: ", user_data)
    user = await _services.authenticate_user(email=user_data.email, password=user_data.password, db=db)
    
    if user == "is_active_false":
        logging.info('Your email account is currently deactivated. Please contact admin to activate your account. ')
        raise _fastapi.HTTPException(
            status_code=403, detail="Your email account is currently deactivated. Please contact admin to activate your account.")

    if not user:
        logging.info('Invalid Credentials')
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Credentials")
    
    
    logging.info('Generating JWT Token')
    
    return await _services.create_token(user=user)


@router.get("/users/me", response_model=_schemas.User  , tags = ['User Auth'])
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user

@router.post("/auth/generate-otp", response_model=str, tags=["User Auth"])
async def send_otp_mail(userdata: _schemas.GenerateOtp, db: _orm.Session = _fastapi.Depends(_database.get_db)):
    user = await _services.get_user_by_email(email=userdata.email, db=db)

    if not user:
        raise _fastapi.HTTPException(status_code=404, detail="User not found")

    if not user.is_active:
        raise _fastapi.HTTPException(status_code=400, detail="User is already activated")

    # Generate and send OTP
    otp = _services.generate_otp()
    
    
    _services.send_otp(userdata.email, otp)

    # Store the OTP in the database
    user.otp = otp
    db.add(user)
    db.commit()

    return "OTP sent to your email"


@router.post("/auth/verify-otp", tags=["User Auth"])
async def verify_otp(userdata: _schemas.VerifyOtp, db: _orm.Session = _fastapi.Depends(_database.get_db)):
    user = await _services.get_user_by_email(email=userdata.email, db=db )

    if not user:
        raise _fastapi.HTTPException(status_code=404, detail="User not found")

    if not user.otp or user.otp != userdata.otp:
        raise _fastapi.HTTPException(status_code=400, detail="Invalid OTP")

    # Update user's is_verified field
    user.is_verified = True
    user.otp = None  # Clear the OTP
    db.add(user)
    db.commit()

    return "Email verified successfully"