from src.log.domain.log import Log
from src.log.infrastructure.repositories.log_model import LogModel


class LogMapper:
    """Convierte entre la entidad de dominio y el modelo de persistencia."""

    @staticmethod
    def to_domain(model: LogModel) -> Log:
        return Log(
            id=model.id,
            action=model.action,
            entity_type=model.entity_type,
            entity_id=model.entity_id,
            description=model.description,
            created_at=model.created_at
        )

    @staticmethod
    def to_model(log: Log) -> LogModel:
        return LogModel(
            id=log.id,
            entity_type=log.entity_type,
            entity_id=log.entity_id,
            action=log.action,
            description=log.description,
            created_at=log.created_at
        )
