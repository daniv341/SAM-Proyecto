from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Column, DateTime

from sqlmodel import SQLModel, Field

from src.vulnerabilitie.domain.vulnerabilitie import Severity


class VulnerabilitieModel(SQLModel, table=True):
    """
    Modelo de base de datos para Vulnerabilitie.
    Pertenece a la capa de infraestructura, separado de la entidad de dominio.
    """
    __tablename__ = "vulnerabilities"

    id: str = Field(primary_key=True)
    cve: str = Field(max_length=100, index=True)
    description: Optional[str] = Field(max_length=200, index=True)
    severity: Severity = Field(Severity.LOW, index=True)
    url: str = Field(max_length=100, index=True)
    mitigation: bool = Field(default=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
