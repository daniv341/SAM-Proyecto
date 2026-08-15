from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.vulnerabilitie.domain.vulnerabilitie import Vulnerabilitie
from src.vulnerabilitie.domain.vulnerabilitie_repository import VulnerabilitieRepository
from src.vulnerabilitie.infrastructure.repositories.vulnerabilitie_mapper import VulnerabilitieMapper
from src.vulnerabilitie.infrastructure.repositories.vulnerabilitie_model import VulnerabilitieModel
from src.workstation.infrastructure.repositories.vulnerabilitie_workstation_model import VulnerabilityWorkstationModel


class SQLAlchemyVulnerabilitieRepository(VulnerabilitieRepository):
    """
    Adaptador de salida (driven adapter).
    Implementación concreta del repositorio usando SQLAlchemy + SQLModel.
    """

    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, vulnerabilitie: Vulnerabilitie) -> Vulnerabilitie:
        model = VulnerabilitieMapper.to_model(vulnerabilitie)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return VulnerabilitieMapper.to_domain(model)

    async def find_by_id(self, vulnerabilitie_id: str) -> Vulnerabilitie | None:
        result = await self._session.execute(
            select(VulnerabilitieModel).where(VulnerabilitieModel.id == vulnerabilitie_id)
        )
        model = result.scalar_one_or_none()
        return VulnerabilitieMapper.to_domain(model) if model else None

    async def find_all(self, skip: int = 0, limit: int = 20) -> list[Vulnerabilitie]:
        result = await self._session.execute(
            select(VulnerabilitieModel).offset(skip).limit(limit)
        )
        models = result.scalars().all()
        return [VulnerabilitieMapper.to_domain(m) for m in models]

    async def update(self, vulnerabilitie: Vulnerabilitie) -> Vulnerabilitie:
        result = await self._session.execute(
            select(VulnerabilitieModel).where(VulnerabilitieModel.id == vulnerabilitie.id)
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"VulnerabilitieModel con id \"{vulnerabilitie.id}\" no encontrado.")

        model.description = vulnerabilitie.description
        model.mitigation = vulnerabilitie.mitigation
        model.updated_at = vulnerabilitie.updated_at

        await self._session.flush()
        await self._session.refresh(model)
        return VulnerabilitieMapper.to_domain(model)

    async def delete(self, vulnerabilitie_id: str) -> None:
        result = await self._session.execute(
            select(VulnerabilitieModel).where(VulnerabilitieModel.id == vulnerabilitie_id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()

    # Devuelve una lista de workstations asociadas a una vulnerabilitie.
    async def find_workstations(self, vulnerability_id: str) -> list[str]:
        result = await self._session.execute(
            select(VulnerabilityWorkstationModel.workstation_id).where(VulnerabilityWorkstationModel.vulnerability_id == vulnerability_id))

        return list(result.scalars().all())