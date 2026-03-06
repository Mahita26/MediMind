from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models import Patient, User
from auth import require_doctor, get_current_user
from schemas import PatientCreate, PatientOut

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.get("", response_model=list[PatientOut])
async def list_patients(
    doctor: User = Depends(require_doctor),
    db: AsyncSession = Depends(get_db),
):
    """Doctor: list all their managed patients."""
    result = await db.execute(
        select(Patient).where(Patient.created_by_doctor_id == doctor.id)
    )
    return result.scalars().all()


@router.post("", response_model=PatientOut, status_code=201)
async def create_patient(
    payload: PatientCreate,
    doctor: User = Depends(require_doctor),
    db: AsyncSession = Depends(get_db),
):
    """Doctor: create a new patient profile."""
    patient = Patient(
        created_by_doctor_id=doctor.id,
        name=payload.name,
        age=payload.age,
        phone=payload.phone,
    )
    db.add(patient)
    await db.flush()
    await db.refresh(patient)
    return patient


@router.get("/{patient_id}", response_model=PatientOut)
async def get_patient(
    patient_id: str,
    doctor: User = Depends(require_doctor),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Patient).where(
            Patient.id == patient_id,
            Patient.created_by_doctor_id == doctor.id
        )
    )
    patient = result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found.")
    return patient
