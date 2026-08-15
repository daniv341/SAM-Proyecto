from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from src.workstation.domain.workstation import Workstation
from src.workstation.domain.workstation_repository import WorkstationRepository
from src.workstation.infrastructure.repositories.workstation_mapper import WorkstationMapper
from src.workstation.infrastructure.repositories.workstation_model import WorkstationModel
from src.workstation.infrastructure.repositories.vulnerabilitie_workstation_model import VulnerabilityWorkstationModel

from src.workstation.application.ports.workstation_dtos import WorkstationFilterDTO

class SQLAlchemyWorkstationRepository(WorkstationRepository):
    """
    Adaptador de salida (driven adapter).
    Implementación concreta del repositorio usando SQLAlchemy + SQLModel.
    """

    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, workstation: Workstation) -> Workstation:
        model = WorkstationMapper.to_model(workstation)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return WorkstationMapper.to_domain(model)

    async def find_by_id(self, workstation_id: str) -> Workstation | None:
        result = await self._session.execute(
            select(WorkstationModel).where(WorkstationModel.id == workstation_id)
        )
        model = result.scalar_one_or_none()
        return WorkstationMapper.to_domain(model) if model else None

    async def find_all(self, filters: WorkstationFilterDTO | None = None, skip: int = 0, limit: int = 20) -> list[Workstation]:
        statement = select(WorkstationModel)

        if filters:
            if filters.user:
                statement = statement.where(WorkstationModel.user == filters.user)
            if filters.status:
                statement = statement.where(WorkstationModel.status == filters.status)
            if filters.type:
                statement = statement.where(WorkstationModel.type == filters.type)
            if filters.area:
                statement = statement.where(WorkstationModel.area == filters.area)
            if filters.created_at:
                statement = statement.where(WorkstationModel.created_at >= filters.created_at)

        result = await self._session.execute(statement.offset(skip).limit(limit))
        models = result.scalars().all()
        return[WorkstationMapper.to_domain(m) for m in models]

    async def update(self, workstation: Workstation) -> Workstation:
        result = await self._session.execute(
            select(WorkstationModel).where(WorkstationModel.id == workstation.id)
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"WorkstationModel con id \"{workstation.id}\" no encontrado.")

        model.user = workstation.user
        model.description = workstation.description
        model.status = workstation.status
        model.type = workstation.type
        model.area = workstation.area
        model.updated_at = workstation.updated_at

        await self._session.flush()
        await self._session.refresh(model)
        return WorkstationMapper.to_domain(model)

    async def delete(self, workstation_id: str) -> None:
        result = await self._session.execute(
            select(WorkstationModel).where(WorkstationModel.id == workstation_id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()

    # añade una vulnerabilidad a un workstation.
    async def add_vulnerability(self, workstation_id: str, vulnerability_id: str) -> None:
        association = VulnerabilityWorkstationModel(workstation_id=workstation_id, vulnerability_id=vulnerability_id)

        self._session.add(association)
        await self._session.commit()

    # elimina una vulnerabilidad de un workstation.
    async def remove_vulnerability(self, workstation_id: str, vulnerability_id: str) -> None:
        result = await self._session.execute(
            select(VulnerabilityWorkstationModel).where(
                VulnerabilityWorkstationModel.workstation_id == workstation_id, VulnerabilityWorkstationModel.vulnerability_id == vulnerability_id))

        association = result.scalar_one_or_none()

        if association:
            await self._session.delete(association)
            await self._session.commit()

    # devuelve una lista de vulnerabilities asociadas a un workstation.
    async def find_vulnerabilities(self, workstation_id: str) -> list[str]: 
        result = await self._session.execute(
            select(VulnerabilityWorkstationModel.vulnerability_id).where(
            VulnerabilityWorkstationModel.workstation_id == workstation_id))

        return list(result.scalars().all())
