from datetime import datetime
from pydantic import BaseModel

from src.log.domain.log import AuditAction, EntityType


class CreateLogDTO(BaseModel):
    action: AuditAction
    entity_type: EntityType
    entity_id: str
    description: str


class LogResponseDTO(BaseModel):
    id: str
    action: AuditAction
    entity_type: EntityType
    entity_id: str
    description: str
    created_at: datetime

    model_config = {"from_attributes": True}


class LogListResponseDTO(BaseModel):
    logs: list[LogResponseDTO]
    total: int
    skip: int
    limit: int
