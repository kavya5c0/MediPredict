from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from app.core.security import (
    verify_password, get_password_hash, create_access_token, get_current_user
)
from app.core.database import users_collection
from app.core.config import settings
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/register")
async def register(user_data: dict):
    """Register a new user"""
    if users_collection is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available. Please ensure MongoDB is running."
        )
    
    # Check if user exists
    existing_user = await users_collection.find_one({"email": user_data["email"]})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    user_data["password"] = get_password_hash(user_data["password"])
    
    # Create user
    user_data["created_at"] = datetime.utcnow()
    user_data["conditions"] = []
    user_data["medications"] = []
    user_data["health_profile"] = {}
    
    result = await users_collection.insert_one(user_data)
    
    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id)
    }

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login user and return access token"""
    if users_collection is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available. Please ensure MongoDB is running."
        )
    
    user = await users_collection.find_one({"email": form_data.username})
    
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user["_id"])}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(user["_id"])
    }

@router.get("/me")
async def get_me(current_user: str = Depends(get_current_user)):
    """Get current user information"""
    if users_collection is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available. Please ensure MongoDB is running."
        )
    
    user = await users_collection.find_one({"_id": ObjectId(current_user)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.pop("password", None)
    user["_id"] = str(user["_id"])
    
    return user
