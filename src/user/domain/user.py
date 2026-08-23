from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

from src.shared.exceptions.domain_exceptions import InvalidValueException

from src.user.domain.user_validate import Name, Email, Password

class Role(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    BANNED = "BANNED"


@dataclass
class User:
    """
    Entidad de dominio User.
    No tiene dependencias de frameworks externos.
    """
    id: str
    name: str
    email: str
    password: str
    role: Role = Role.USER
    date_of_birth: datetime | None = None
    status: UserStatus = UserStatus.ACTIVE
    bio: str | None = None
    image_url: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        self.name = Name(self.name).value
        self.email = Email(self.email).value
        self.password = Password(self.password).value

    def banned_changed_to_suspended(self, new_status: UserStatus):
        if (self.status == UserStatus.BANNED
            and new_status == UserStatus.SUSPENDED):
            raise InvalidValueException("Un user baneado no puede ser suspendido.")

        self.status = new_status

    def _touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc)
