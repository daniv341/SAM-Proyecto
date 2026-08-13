from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

from src.shared.exceptions.domain_exceptions import InvalidValueException

from src.vulnerabilitie.domain.vulnerabilitie_validate import Description, CVE

class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class Vulnerabilitie:
    """
    Entidad de dominio Vulnerabilitie.
    No tiene dependencias de frameworks externos.
    """
    id: str
    cve: str
    description: str
    severity: Severity
    url: str
    mitigation: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        if self.description is not None:
            self.description = Description(self.description).value
        self.cve = CVE(self.cve).value

    def _touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc)
