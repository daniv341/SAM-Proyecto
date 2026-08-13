from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator

from src.user.domain.user import UserStatus

from src.user.domain.user_validate import Name, Email, Password


class CreateUserDTO(BaseModel):
    name: str
    email: str
    password: str
    date_of_birth: datetime
    bio: str | None = None
    image_url: str | None = None

    @field_validator("name")
    @classmethod
    def name_must_be_valid(cls, v):
        return Name(v).value

    @field_validator("email")
    @classmethod
    def email_must_be_valid(cls, v):
        return Email(v).value

    @field_validator("password")
    @classmethod
    def password_must_be_valid(cls, v):
        return Password(v).value



class UpdateUserDTO(BaseModel):
    password: str | None = None
    status: UserStatus | None = None
    bio: str | None = None
    image_url: str | None = None

    @field_validator("password")
    @classmethod
    def password_must_be_valid(cls, v):
        return Password(v).value


class UserResponseDTO(BaseModel):
    id: str
    name: str
    email: str
    date_of_birth: datetime
    status: UserStatus
    bio: str | None = None
    image_url: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

# este DTO es para el inicio de sesion, es decir, para recibir el email y la contraseña del usuario que quiere iniciar sesion
class LoginDTO(BaseModel):
    email: EmailStr
    password: str


# este DTO es para la respuesta del inicio de sesion(LoginDTO), que incluye el token de acceso
class TokenResponseDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponseShort(BaseModel):
    id: str
    name: str

    model_config = {"from_attributes": True}

class UserListResponseDTO(BaseModel):
    users: list[UserResponseDTO]
    total: int
    skip: int
    limit: int
