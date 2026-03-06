"""
Gmail OAuth2 Integration for user authentication.
Allows users to authenticate using their real Gmail accounts.
"""

import os
from typing import Optional
from google.auth.transport.requests import Request
from google.oauth2.id_token import verify_oauth2_token
from google.oauth2 import service_account
from fastapi import HTTPException, status

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:3000/auth/callback")


def verify_gmail_token(token: str) -> dict:
    """
    Verify Google OAuth2 ID token from Google Sign-In.
    
    Args:
        token: ID token from Google Sign-In frontend
        
    Returns:
        User info dict containing email, name, picture, etc.
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        idinfo = verify_oauth2_token(token, Request(), GOOGLE_CLIENT_ID)
        
        # Verify token is for our app
        if idinfo['aud'] != GOOGLE_CLIENT_ID:
            raise ValueError('Token was not issued for this application.')
            
        # Token is valid - return user info
        return {
            'email': idinfo.get('email'),
            'name': idinfo.get('name'),
            'picture': idinfo.get('picture'),
            'email_verified': idinfo.get('email_verified', False),
            'google_id': idinfo.get('sub')
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Gmail token: {str(e)}"
        )


def validate_gmail_address(email: str) -> bool:
    """Validate if email is a real Gmail address."""
    return email.endswith("@gmail.com") or email.endswith("@googlemail.com")
