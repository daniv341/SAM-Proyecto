from src.workstation.domain.workstation import Workstation
from src.workstation.infrastructure.repositories.workstation_model import WorkstationModel


class WorkstationMapper:
    """Convierte entre la entidad de dominio y el modelo de persistencia."""

    @staticmethod
    def to_domain(model: WorkstationModel) -> Workstation:
        return Workstation(
            id=model.id,
            user=model.user,
            description=model.description,
            status=model.status,
            type=model.type,
            area=model.area,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(workstation: Workstation) -> WorkstationModel:
        return WorkstationModel(
            id=workstation.id,
            user=workstation.user,
            description=workstation.description,
            status=workstation.status,
            type=workstation.type,
            area=workstation.area,
            created_at=workstation.created_at,
            updated_at=workstation.updated_at,
        )
