from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Column, DateTime

from sqlmodel import SQLModel, Field

from src.log.domain.log import AuditAction, EntityType


class LogModel(SQLModel, table=True):
    """
    Modelo de base de datos para Log.
    Pertenece a la capa de infraestructura, separado de la entidad de dominio.
    """
    __tablename__ = "logs"

    id: str = Field(primary_key=True)
    action: AuditAction = Field(default=AuditAction.CREATE, index=True)
    entity_type: EntityType = Field(default=EntityType.USER, index=True)
    entity_id: str = Field(default=None, max_length=50, index=True)
    description: str = Field(default=None, max_length=100, index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
