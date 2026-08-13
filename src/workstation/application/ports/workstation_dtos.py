from datetime import datetime
from pydantic import BaseModel, field_validator

from src.workstation.domain.workstation import WorkstationStatus, Type, Area

from src.user.application.ports.user_dtos import UserResponseShort

from src.workstation.domain.workstation_validate import Description

class CreateWorkstationDTO(BaseModel):
    user: str
    description: str | None = None
    type: Type
    area: Area

    @field_validator("description")
    @classmethod
    def description_must_be_valid(cls, v):
        return Description(v).value


class UpdateWorkstationDTO(BaseModel):
    user: str | None = None
    description: str | None = None
    status: WorkstationStatus | None = None
    type: Type | None = None
    area: Area | None = None

    @field_validator("description")
    @classmethod
    def description_must_be_valid(cls, v):
        return Description(v).value


class WorkstationResponseDTO(BaseModel):
    id: str
    user: UserResponseShort
    description: str | None = None
    status: WorkstationStatus
    type: Type
    area: Area
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class WorkstationListResponseDTO(BaseModel):
    workstations: list[WorkstationResponseDTO]
    total: int
    skip: int
    limit: int
