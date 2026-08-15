from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

from src.shared.exceptions.domain_exceptions import InvalidValueException

# si quieres un ejemplo de como se debe agregar el log en cada caso de uso donde quieras registrar una accion, ve a created_user y la dependencies de dicho caso de uso

class AuditAction(str, Enum):
    CREATE = "CREATE"
    GET = "GET"
    GETALL = "GETALL"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    ALERT = "ALERT"

class EntityType(str, Enum):
    USER = "USER"
    WORKSTATION = "WORKSTATION"
    VULNERABILTIE = "VULNERABILITIE"

@dataclass
class Log:
    """
    Entidad de dominio Log.
    No tiene dependencias de frameworks externos.
    """
    id: str
    action: AuditAction
    entity_type: EntityType
    entity_id: str
    description: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

