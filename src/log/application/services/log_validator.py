"""
Funciones auxiliares de validación para Log.

Propósito: centralizar las validaciones de unicidad, existencia de FKs
y construcción del ResponseDTO enriquecido con datos de objetos relacionados.
Estas funciones son llamadas desde los casos de uso (create, update, get).

── Cómo extender este archivo ────────────────────────────────────────────────
1. Agrega el repositorio de cada objeto relacionado como parámetro de la función.
2. En _to_log_unicity   → verifica que campos únicos no estén ya en uso.
3. En _to_log_validator → verifica que cada FK exista antes de crear.
4. En _to_update_log_validator → igual que el anterior pero sin chequear
   campos que no se pueden cambiar en un update (ej: user_id).
5. En _to_log_response  → carga los objetos relacionados y construye el DTO
   con sus respectivos sub-DTOs (ej: GameResponseShortDTO, RegionResponseShortDTO).
──────────────────────────────────────────────────────────────────────────────
"""
from src.log.domain.log import Log
from src.log.domain.log_repository import LogRepository
from src.log.application.ports.log_dtos import LogResponseDTO
from src.shared.exceptions.domain_exceptions import (
    EntityNotFoundException,
    EntityAlreadyExistsException,
)

# TODO: importar los repositorios de los objetos relacionados, por ejemplo:
# from src.<related>.domain.<related>_repository import <Related>Repository

# TODO: importar los sub-DTOs de los objetos relacionados, por ejemplo:
# from src.<related>.application.ports.<related>_dtos import <Related>ResponseShortDTO


async def _to_log_unicity(
    log: Log,
    log_repository: LogRepository,
) -> None:
    """
    Verifica que los campos únicos del log no estén ya registrados.
    Lanza EntityAlreadyExistsException si encuentra un duplicado.

    TODO: agregar una verificación por cada campo único del objeto, por ejemplo:

        existing = await log_repository.find_by_name(log.name)
        if existing:
            raise EntityAlreadyExistsException("Log", "name", log.name)
    """
    pass


async def _to_log_validator(
    log: Log,
    # TODO: agregar los repositorios de FKs como parámetros, por ejemplo:
    # related_repository: RelatedRepository,
) -> None:
    """
    Verifica que todos los objetos referenciados por FKs existan en la BD.
    Úsala en el caso de uso de creación antes de llamar a repo.save().
    Lanza EntityNotFoundException si alguna FK no existe.

    TODO: agregar una verificación por cada FK del objeto, por ejemplo:

        related = await related_repository.find_by_id(log.related_id)
        if not related:
            raise EntityNotFoundException("Related", log.related_id)
    """
    pass


async def _to_update_log_validator(
    log: Log,
    # TODO: agregar los repositorios de FKs actualizables como parámetros.
    # Generalmente son los mismos que _to_log_validator, excepto los campos
    # que no se pueden cambiar en un update (ej: user_id, owner_id).
) -> None:
    """
    Igual que _to_log_validator pero aplicado al flujo de actualización.
    Solo valida las FKs que se permiten modificar.

    TODO: agregar verificaciones para cada FK que sea editable, por ejemplo:

        if log.related_id:
            related = await related_repository.find_by_id(log.related_id)
            if not related:
                raise EntityNotFoundException("Related", log.related_id)
    """
    pass


async def _to_log_response(
    log: Log,
    # TODO: agregar los repositorios necesarios para cargar los datos relacionados.
) -> LogResponseDTO:
    """
    Construye el LogResponseDTO cargando los datos de los objetos
    relacionados. Úsala al final de los casos de uso create, update y get
    en lugar de construir el DTO directamente.

    TODO: cargar cada objeto relacionado y pasarlo como sub-DTO al ResponseDTO.
    Ejemplo:

        related = await related_repository.find_by_id(log.related_id)
        if not related:
            raise EntityNotFoundException("Related", log.related_id)

        return LogResponseDTO(
            id=log.id,
            name=log.name,
            status=log.status,
            related=RelatedResponseShortDTO(field=related.field),
            created_at=log.created_at,
            updated_at=log.updated_at,
        )
    """
    # Implementación base sin relaciones (reemplazar con la versión completa)
    return LogResponseDTO(
        id=log.id,
        name=log.name,
        status=log.status,
        created_at=log.created_at,
        updated_at=log.updated_at,
    )
