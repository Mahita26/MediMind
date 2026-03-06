from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import Optional

from database import get_db
from models import Scan, Patient, User
from auth import get_current_user
from schemas import ScanOut
from services import ai_service, generate_radiology_report, generate_patient_explanation

router = APIRouter(prefix="/scans", tags=["Scans"])


@router.post("/upload", response_model=ScanOut, status_code=201)
async def upload_scan(
    file: UploadFile = File(...),
    patient_profile_id: Optional[str] = Query(None, description="For doctors: the managed patient ID"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload an X-ray and run AI inference.
    - **Doctor**: must supply `patient_profile_id`. Scan is linked to that patient.
    - **Patient**: uploads for themselves (no `patient_profile_id` needed).
    """
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are accepted.")

    image_bytes = await file.read()

    # Determine which user account this scan belongs to
    patient_name_snapshot: Optional[str] = None

    if current_user.role == "doctor":
        if not patient_profile_id:
            raise HTTPException(status_code=400, detail="Doctors must supply a patient_profile_id.")
        # Verify doctor owns this patient
        result = await db.execute(
            select(Patient).where(
                Patient.id == patient_profile_id,
                Patient.created_by_doctor_id == current_user.id,
            )
        )
        patient_profile = result.scalar_one_or_none()
        if not patient_profile:
            raise HTTPException(status_code=404, detail="Patient not found or access denied.")

        patient_name_snapshot = patient_profile.name
        # Use patient_profile.patient_user_id if they have an account, else doctor's id as placeholder
        owner_user_id = patient_profile.patient_user_id or current_user.id
    else:
        # Patient uploads for themselves
        owner_user_id = current_user.id
        patient_name_snapshot = current_user.full_name
        patient_profile_id = None

    # ── AI Inference ─────────────────────────────────────────────────────────
    predictions = ai_service.predict(image_bytes)
    heatmap_b64 = ai_service.generate_heatmap(image_bytes)
    report = generate_radiology_report(predictions)
    explanation = generate_patient_explanation(report)

    # ── Persist Scan ──────────────────────────────────────────────────────────
    scan = Scan(
        patient_user_id=owner_user_id,
        uploaded_by_id=current_user.id,
        patient_profile_id=patient_profile_id,
        patient_name=patient_name_snapshot,
        predictions=predictions,
        report_findings=report["findings"],
        report_impression=report["impression"],
        report_recommendation=report["recommendation"],
        patient_explanation=explanation,
        heatmap_base64=heatmap_b64,
    )
    db.add(scan)
    await db.flush()
    await db.refresh(scan)

    return ScanOut.from_orm_scan(scan)


@router.get("/history", response_model=list[ScanOut])
async def get_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Returns scan history.
    - **Doctor**: sees scans uploaded by themselves.
    - **Patient**: sees only their own scans.
    """
    if current_user.role == "doctor":
        result = await db.execute(
            select(Scan)
            .where(Scan.uploaded_by_id == current_user.id)
            .order_by(Scan.created_at.desc())
        )
    else:
        result = await db.execute(
            select(Scan)
            .where(Scan.patient_user_id == current_user.id)
            .order_by(Scan.created_at.desc())
        )
    scans = result.scalars().all()
    return [ScanOut.from_orm_scan(s) for s in scans]


@router.get("/{scan_id}", response_model=ScanOut)
async def get_scan(
    scan_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Access-controlled: patients can only view their own scans."""
    result = await db.execute(select(Scan).where(Scan.id == scan_id))
    scan = result.scalar_one_or_none()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found.")

    # Security: patient can only see their own scans; doctor can see scans they uploaded
    if current_user.role == "patient" and scan.patient_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied.")
    if current_user.role == "doctor" and scan.uploaded_by_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied.")

    return ScanOut.from_orm_scan(scan)
