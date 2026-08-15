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


# dto para los filtros en el get all
class LogFilterDTO(BaseModel):
    action: AuditAction | None = None
    entity_type: EntityType | None = None
    entity_id: str | None = None
    created_at: datetime | None = None

