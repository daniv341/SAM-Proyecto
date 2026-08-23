from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Column, DateTime

from sqlmodel import SQLModel, Field

from src.user.domain.user import Role, UserStatus


class UserModel(SQLModel, table=True):
    """
    Modelo de base de datos para User.
    Pertenece a la capa de infraestructura, separado de la entidad de dominio.
    """
    __tablename__ = "users"

    id: str = Field(primary_key=True)
    name: str = Field(max_length=100, index=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password: str = Field(max_length=255)
    date_of_birth: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    role: Role = Field(default=Role.USER)
    status: UserStatus = Field(default=UserStatus.ACTIVE)
    bio: Optional[str] = Field(default=None)
    image_url: Optional[str] = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
