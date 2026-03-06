import uuid
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, Enum, Text, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


def gen_uuid() -> str:
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(Enum("doctor", "patient", name="user_role"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    patients_created: Mapped[list["Patient"]] = relationship(
        "Patient", foreign_keys="Patient.created_by_doctor_id", back_populates="doctor"
    )
    scans_as_patient: Mapped[list["Scan"]] = relationship(
        "Scan", foreign_keys="Scan.patient_user_id", back_populates="patient_user"
    )


class Patient(Base):
    """Doctor-managed patient profile (doesn't require a user account)."""
    __tablename__ = "patients"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    created_by_doctor_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    # Optional link: if this patient also registers as a User
    patient_user_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    phone: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    doctor: Mapped["User"] = relationship("User", foreign_keys=[created_by_doctor_id], back_populates="patients_created")


class Scan(Base):
    __tablename__ = "scans"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    # Who this scan belongs to (a user account)
    patient_user_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    # Who uploaded it (doctor or patient themselves)
    uploaded_by_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    # If uploaded by a doctor for a managed patient (not yet a registered user),
    # store the patient profile id
    patient_profile_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("patients.id", ondelete="SET NULL"), nullable=True
    )
    patient_name: Mapped[str | None] = mapped_column(String, nullable=True)  # snapshot
    predictions: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    report_findings: Mapped[str | None] = mapped_column(Text, nullable=True)
    report_impression: Mapped[str | None] = mapped_column(Text, nullable=True)
    report_recommendation: Mapped[str | None] = mapped_column(Text, nullable=True)
    patient_explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    heatmap_base64: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    patient_user: Mapped["User"] = relationship(
        "User", foreign_keys=[patient_user_id], back_populates="scans_as_patient"
    )
