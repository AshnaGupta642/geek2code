from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class PatientCaregiver(Base):
    __tablename__ = "patient_caregivers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"),
        nullable=False
    )

    caregiver_id: Mapped[int] = mapped_column(
        ForeignKey("caregivers.id"),
        nullable=False
    )