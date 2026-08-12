from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.workstation.domain.workstation import Workstation
from src.workstation.domain.workstation_repository import WorkstationRepository
from src.workstation.infrastructure.repositories.workstation_mapper import WorkstationMapper
from src.workstation.infrastructure.repositories.workstation_model import WorkstationModel


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

    async def find_all(self, skip: int = 0, limit: int = 20) -> list[Workstation]:
        result = await self._session.execute(
            select(WorkstationModel).offset(skip).limit(limit)
        )
        models = result.scalars().all()
        return [WorkstationMapper.to_domain(m) for m in models]

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
