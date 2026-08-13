from src.vulnerabilitie.domain.vulnerabilitie import Vulnerabilitie
from src.vulnerabilitie.infrastructure.repositories.vulnerabilitie_model import VulnerabilitieModel


class VulnerabilitieMapper:
    """Convierte entre la entidad de dominio y el modelo de persistencia."""

    @staticmethod
    def to_domain(model: VulnerabilitieModel) -> Vulnerabilitie:
        return Vulnerabilitie(
            id=model.id,
            cve=model.cve,
            description=model.description,
            severity=model.severity,
            url=model.url,
            mitigation=model.mitigation,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(vulnerabilitie: Vulnerabilitie) -> VulnerabilitieModel:
        return VulnerabilitieModel(
            id=vulnerabilitie.id,
            cve=vulnerabilitie.cve,
            description=vulnerabilitie.description,
            severity=vulnerabilitie.severity,
            url=vulnerabilitie.url,
            mitigation=vulnerabilitie.mitigation,
            created_at=vulnerabilitie.created_at,
            updated_at=vulnerabilitie.updated_at,
        )
