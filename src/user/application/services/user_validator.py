from src.user.domain.user import User
from src.user.domain.user_repository import UserRepository
from src.user.application.ports.user_dtos import UserResponseDTO
from src.shared.exceptions.domain_exceptions import (
    EntityNotFoundException,
    EntityAlreadyExistsException,
)


async def _to_user_unicity(
    user: User,
    user_repository: UserRepository,
) -> None:
    """
    Verifica que los campos únicos del user no estén ya registrados.
    Lanza EntityAlreadyExistsException si encuentra un duplicado.

    TODO: agregar una verificación por cada campo único del objeto, por ejemplo:

        existing = await user_repository.find_by_name(user.name)
        if existing:
            raise EntityAlreadyExistsException("User", "name", user.name)
    """
    pass


async def _to_user_validator(
    user: User,
    # TODO: agregar los repositorios de FKs como parámetros, por ejemplo:
    # related_repository: RelatedRepository,
) -> None:
    """
    Verifica que todos los objetos referenciados por FKs existan en la BD.
    Úsala en el caso de uso de creación antes de llamar a repo.save().
    Lanza EntityNotFoundException si alguna FK no existe.

    TODO: agregar una verificación por cada FK del objeto, por ejemplo:

        related = await related_repository.find_by_id(user.related_id)
        if not related:
            raise EntityNotFoundException("Related", user.related_id)
    """
    pass


async def _to_update_user_validator(
    user: User,
    # TODO: agregar los repositorios de FKs actualizables como parámetros.
    # Generalmente son los mismos que _to_user_validator, excepto los campos
    # que no se pueden cambiar en un update (ej: user_id, owner_id).
) -> None:
    """
    Igual que _to_user_validator pero aplicado al flujo de actualización.
    Solo valida las FKs que se permiten modificar.

    TODO: agregar verificaciones para cada FK que sea editable, por ejemplo:

        if user.related_id:
            related = await related_repository.find_by_id(user.related_id)
            if not related:
                raise EntityNotFoundException("Related", user.related_id)
    """
    pass


async def _to_user_response(
    user: User,
    # TODO: agregar los repositorios necesarios para cargar los datos relacionados.
) -> UserResponseDTO:
    """
    Construye el UserResponseDTO cargando los datos de los objetos
    relacionados. Úsala al final de los casos de uso create, update y get
    en lugar de construir el DTO directamente.

    TODO: cargar cada objeto relacionado y pasarlo como sub-DTO al ResponseDTO.
    Ejemplo:

        related = await related_repository.find_by_id(user.related_id)
        if not related:
            raise EntityNotFoundException("Related", user.related_id)

        return UserResponseDTO(
            id=user.id,
            name=user.name,
            status=user.status,
            related=RelatedResponseShortDTO(field=related.field),
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
    """
    # Implementación base sin relaciones (reemplazar con la versión completa)
    return UserResponseDTO(
        id=user.id,
        name=user.name,
        status=user.status,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
