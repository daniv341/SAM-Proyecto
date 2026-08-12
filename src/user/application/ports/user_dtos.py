from datetime import datetime
from pydantic import BaseModel, field_validator

from src.user.domain.user import UserStatus

from src.user.domain.user_validate import Name


class CreateUserDTO(BaseModel):
    name: str
    date_of_birth: datetime
    bio: str | None = None
    image_url: str | None = None

    @field_validator("name")
    @classmethod
    def name_must_be_valid(cls, v):
        return Name(v).value



class UpdateUserDTO(BaseModel):
    name: str | None = None
    status: UserStatus | None = None
    bio: str | None = None
    image_url: str | None = None

    @field_validator("name")
    @classmethod
    def name_must_be_valid(cls, v):
        return Name(v).value


class UserResponseDTO(BaseModel):
    id: str
    name: str
    date_of_birth: datetime
    status: UserStatus
    bio: str | None = None
    image_url: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class UserResponseShort(BaseModel):
    id: str
    name: str

    model_config = {"from_attributes": True}

class UserListResponseDTO(BaseModel):
    users: list[UserResponseDTO]
    total: int
    skip: int
    limit: int
