from src.workstation.domain.workstation import Workstation
from src.workstation.domain.workstation_repository import WorkstationRepository
from src.workstation.application.ports.workstation_dtos import WorkstationResponseDTO
from src.shared.exceptions.domain_exceptions import (
    EntityNotFoundException,
    EntityAlreadyExistsException,
)

from src.user.domain.user_repository import UserRepository

from src.user.application.ports.user_dtos import UserResponseShort

from src.user.domain.user import User


async def _to_workstation_unicity(
    workstation: Workstation,
    workstation_repository: WorkstationRepository,
) -> None:
    """
    Verifica que los campos únicos del workstation no estén ya registrados.
    Lanza EntityAlreadyExistsException si encuentra un duplicado.

    TODO: agregar una verificación por cada campo único del objeto, por ejemplo:

        existing = await workstation_repository.find_by_name(workstation.name)
        if existing:
            raise EntityAlreadyExistsException("Workstation", "name", workstation.name)
    """
    pass


async def _to_workstation_validator(workstation: Workstation, user_repository: UserRepository,
) -> User:
    # comprobar que el workstation exista, de lo contrario lanza error
    user = await user_repository.find_by_id(workstation.user)
    if not user:
        raise EntityNotFoundException("User", workstation.user)

    return user


async def _to_update_workstation_validator(workstation: Workstation, user_repository: UserRepository,) -> User | None:
    user = None
    print("workstation.user", workstation.user)
    # comprobar que el workstation exista, de lo contrario lanza error
    user = await user_repository.find_by_id(workstation.user)
    if not user:
        raise EntityNotFoundException("User", workstation.user)
    
    return user


async def _to_workstation_response(workstation: Workstation, user_repository: UserRepository,) -> WorkstationResponseDTO:
    # comprobar que el workstation exista, de lo contrario lanza error
    user = await user_repository.find_by_id(workstation.user)
    if not user:
        raise EntityNotFoundException("User", workstation.user)
    
    return WorkstationResponseDTO(
        id=workstation.id,
        user=UserResponseShort(
            id=user.id,
            name=user.name,
        ),
        description=workstation.description,
        status=workstation.status,
        type=workstation.type,
        area=workstation.area,
        created_at=workstation.created_at,
        updated_at=workstation.updated_at,
    )
