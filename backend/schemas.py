from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
import re


# ─── Auth ─────────────────────────────────────────────────────────────────────
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str  # "doctor" or "patient"

    @field_validator("email")
    @classmethod
    def email_must_be_valid(cls, v: str) -> str:
        # Validate email format and preferably use real email domains
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError("Invalid email format")
        # Reject temporary/fake email providers (optional - add more if needed)
        fake_domains = ['test.com', 'fake.com', 'example.com', 'tempmail.com', 'guerrillamail.com']
        domain = v.split('@')[1].lower()
        if domain in fake_domains:
            raise ValueError("Please use a real email address")
        return v
    
    @field_validator("password")
    @classmethod
    def password_must_be_strong(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v

    @field_validator("role")
    @classmethod
    def role_must_be_valid(cls, v: str) -> str:
        if v not in ("doctor", "patient"):
            raise ValueError("role must be 'doctor' or 'patient'")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    full_name: str
    role: str


# ─── User ─────────────────────────────────────────────────────────────────────
class UserOut(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Patient ──────────────────────────────────────────────────────────────────
class PatientCreate(BaseModel):
    name: str
    age: Optional[int] = None
    phone: Optional[str] = None


class PatientOut(BaseModel):
    id: str
    name: str
    age: Optional[int]
    phone: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Scan ─────────────────────────────────────────────────────────────────────
class ReportOut(BaseModel):
    findings: Optional[str]
    impression: Optional[str]
    recommendation: Optional[str]


class ScanOut(BaseModel):
    id: str
    patient_user_id: str
    patient_name: Optional[str]
    predictions: dict
    report: ReportOut
    patient_explanation: Optional[str]
    heatmap_base64: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_scan(cls, scan) -> "ScanOut":
        return cls(
            id=scan.id,
            patient_user_id=scan.patient_user_id,
            patient_name=scan.patient_name,
            predictions=scan.predictions or {},
            report=ReportOut(
                findings=scan.report_findings,
                impression=scan.report_impression,
                recommendation=scan.report_recommendation,
            ),
            patient_explanation=scan.patient_explanation,
            heatmap_base64=scan.heatmap_base64,
            created_at=scan.created_at,
        )


# ─── Stats ────────────────────────────────────────────────────────────────────
class StatsOut(BaseModel):
    total_users: int
    total_scans: int
    accuracy_rate: float
