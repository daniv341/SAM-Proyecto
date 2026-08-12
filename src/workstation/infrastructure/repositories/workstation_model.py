from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Column, DateTime

from sqlmodel import SQLModel, Field

from src.workstation.domain.workstation import WorkstationStatus, Type, Area


class WorkstationModel(SQLModel, table=True):
    """
    Modelo de base de datos para Workstation.
    Pertenece a la capa de infraestructura, separado de la entidad de dominio.
    """
    __tablename__ = "workstations"

    id: str = Field(primary_key=True)
    user: str = Field(foreign_key="users.id", unique=True, index=True)
    description: Optional[str] = Field(max_length=100, index=True)
    status: WorkstationStatus = Field(default=WorkstationStatus.ACTIVE)
    type: Type = Field(default=Type.DESKTOP, index=True)
    area: Area = Field(default=Area.SUPPORT, index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
