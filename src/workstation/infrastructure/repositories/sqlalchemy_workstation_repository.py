from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from src.workstation.domain.workstation import Workstation
from src.workstation.domain.workstation_repository import WorkstationRepository
from src.workstation.infrastructure.repositories.workstation_mapper import WorkstationMapper
from src.workstation.infrastructure.repositories.workstation_model import WorkstationModel
from src.workstation.infrastructure.repositories.vulnerabilitie_workstation_model import VulnerabilitieWorkstationModel

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

    async def find_by_user_id(self, user_id: str) -> list[Workstation]:
        result = await self._session.execute(
            select(WorkstationModel).where(WorkstationModel.user == user_id))
        models = result.scalars().all()
        return [WorkstationMapper.to_domain(m) for m in models]

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

        statement = statement.order_by(WorkstationModel.created_at.desc())

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
    async def add_vulnerabilitie(self, workstation_id: str, vulnerabilitie_id: str) -> None:
        association = VulnerabilitieWorkstationModel(workstation_id=workstation_id, vulnerabilitie_id=vulnerabilitie_id)

        self._session.add(association)
        await self._session.commit()

    #comprueba que la relacion entre una vulnerabilitie y un workstation no exista ya
    async def vulnerabilitie_exists(self, workstation_id: str, vulnerabilitie_id: str) -> bool:
        result = await self._session.execute(                                   select(VulnerabilitieWorkstationModel).where(VulnerabilitieWorkstationModel.workstation_id == workstation_id, VulnerabilitieWorkstationModel.vulnerabilitie_id == vulnerabilitie_id))

        return result.scalar_one_or_none() is not None

    # elimina una vulnerabilidad de un workstation.
    async def remove_vulnerabilitie(self, workstation_id: str, vulnerabilitie_id: str) -> None:
        result = await self._session.execute(
            select(VulnerabilitieWorkstationModel).where(
                VulnerabilitieWorkstationModel.workstation_id == workstation_id, VulnerabilitieWorkstationModel.vulnerabilitie_id == vulnerabilitie_id))

        association = result.scalar_one_or_none()

        if association:
            await self._session.delete(association)
            await self._session.commit()

    # devuelve una lista de vulnerabilities asociadas a un workstation.
    async def find_vulnerabilities(self, workstation_id: str) -> list[str]: 
        result = await self._session.execute(
            select(VulnerabilitieWorkstationModel.vulnerabilitie_id).where(
            VulnerabilitieWorkstationModel.workstation_id == workstation_id))

        return list(result.scalars().all())
