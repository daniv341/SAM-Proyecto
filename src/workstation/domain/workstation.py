from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

from src.shared.exceptions.domain_exceptions import InvalidValueException

from src.workstation.domain.workstation_validate import Description

class WorkstationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    BANNED = "BANNED"

class Type(str, Enum):
    DESKTOP = "DESKTOP"
    NOTEBOOK = "NOTEBOOK"
    MOBILE = "MOBILE"
    TABLET = "TABLET"

class Area(str, Enum):
    DEVELOPMENT = "DEVELOPMENT"
    DESIGN = "DESIGN"
    MARKETING = "MARKETING"
    SALES = "SALES"
    SUPPORT = "SUPPORT"

@dataclass
class Workstation:
    """
    Entidad de dominio Workstation.
    No tiene dependencias de frameworks externos.
    """
    id: str
    user: str
    description: str 
    status: WorkstationStatus = WorkstationStatus.ACTIVE
    type: Type = Type.DESKTOP
    area: Area = Area.DEVELOPMENT
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        if self.description is not None:
            self.description = Description(self.description).value

    def ban(self) -> None:
        if self.status == WorkstationStatus.BANNED:
            return

        self.status = WorkstationStatus.BANNED

    def _touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc)
