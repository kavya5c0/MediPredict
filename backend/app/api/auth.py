from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from app.core.security import (
    verify_password, get_password_hash, create_access_token, get_current_user
)
from app.core.database import get_db, release_db
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/register")
async def register(user_data: dict):
    """Register a new user"""
    try:
        conn = await get_db()
    except Exception:
        # Fallback for demo without database
        import uuid
        user_id = str(uuid.uuid4())
        return {
            "message": "User registered successfully (demo mode - database unavailable)",
            "user_id": user_id
        }
    
    try:
        # Check if user exists
        existing_user = await conn.fetchrow(
            "SELECT id FROM users WHERE email = $1",
            user_data["email"]
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        hashed_password = get_password_hash(user_data["password"])
        
        # Create user
        user_id = await conn.fetchrow("""
            INSERT INTO users (email, password, full_name, age, gender)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id
        """, user_data["email"], hashed_password, user_data.get("full_name"), 
            user_data.get("age"), user_data.get("gender"))
        
        return {
            "message": "User registered successfully",
            "user_id": str(user_id["id"])
        }
    finally:
        await release_db(conn)

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login user and return access token"""
    try:
        conn = await get_db()
    except Exception:
        # Fallback for demo without database
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": "demo-user"}, expires_delta=access_token_expires
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": "demo-user"
        }
    
    try:
        user = await conn.fetchrow(
            "SELECT * FROM users WHERE email = $1",
            form_data.username
        )
        
        if not user or not verify_password(form_data.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user["id"])}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": str(user["id"])
        }
    finally:
        await release_db(conn)

@router.get("/me")
async def get_me(current_user: str = Depends(get_current_user)):
    """Get current user information"""
    conn = await get_db()
    try:
        user = await conn.fetchrow(
            "SELECT id, email, full_name, age, gender, created_at, conditions, medications, health_profile FROM users WHERE id = $1",
            int(current_user)
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_dict = dict(user)
        user_dict.pop("password", None)
        user_dict["id"] = str(user_dict["id"])
        
        return user_dict
    finally:
        await release_db(conn)
