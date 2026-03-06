from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models import User
from auth import hash_password, verify_password, create_access_token
from schemas import RegisterRequest, LoginRequest, TokenResponse
from gmail_oauth import verify_gmail_token, validate_gmail_address

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    # Check email uniqueness
    result = await db.execute(select(User).where(User.email == payload.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered.")

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        role=payload.role,
    )
    db.add(user)
    await db.flush()  # assigns user.id before commit
    await db.refresh(user)

    token = create_access_token({"sub": user.id, "role": user.role})
    return TokenResponse(
        access_token=token,
        user_id=user.id,
        full_name=user.full_name,
        role=user.role,
    )


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = create_access_token({"sub": user.id, "role": user.role})
    return TokenResponse(
        access_token=token,
        user_id=user.id,
        full_name=user.full_name,
        role=user.role,
    )


@router.post("/gmail-login", response_model=TokenResponse)
async def gmail_login(google_token: dict, db: AsyncSession = Depends(get_db)):
    """
    Authenticate using Google OAuth2 token from frontend.
    
    Expected body:
    {
        "token": "<id_token from Google Sign-In>"
    }
    """
    try:
        token_str = google_token.get("token")
        if not token_str:
            raise HTTPException(status_code=400, detail="Missing 'token' field")
            
        # Verify token with Google
        user_info = verify_gmail_token(token_str)
        email = user_info['email']
        
        # Check if user exists
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        
        if not user:
            # Auto-create user from Gmail
            user = User(
                email=email,
                hashed_password="",  # Gmail users don't need password
                full_name=user_info.get('name', email.split('@')[0]),
                role="patient",  # Default role for new Gmail users
            )
            db.add(user)
            await db.flush()
            await db.refresh(user)
        
        # Create JWT token
        token = create_access_token({"sub": user.id, "role": user.role})
        return TokenResponse(
            access_token=token,
            user_id=user.id,
            full_name=user.full_name,
            role=user.role,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gmail login failed: {str(e)}"
        )

