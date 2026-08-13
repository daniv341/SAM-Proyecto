from ulid import ULID

from src.shared.exceptions.domain_exceptions import EntityAlreadyExistsException
from src.user.application.ports.user_dtos import CreateUserDTO, UserResponseDTO
from src.user.domain.user import User
from src.user.domain.user_repository import UserRepository
from src.shared.config.security import hash_password

# debes importar el objeto log junto con su repositorio
from src.log.domain.log import Log
from src.log.domain.log_repository import LogRepository

class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository, log_repository: LogRepository):
        self._repo = user_repository
        self._repo_log = log_repository

    async def execute(self, dto: CreateUserDTO) -> UserResponseDTO:
        existing = await self._repo.find_by_email(dto.email)
        if existing:
            raise EntityAlreadyExistsException("User", "email", dto.email)

        user = User(
            id=str(ULID()),
            name=dto.name,
            email=dto.email,
            password=hash_password(dto.password),
            date_of_birth=dto.date_of_birth,
            bio=dto.bio,
            image_url=dto.image_url,
        )

        saved = await self._repo.save(user)

        # de esta forma es como se debe crear un registro en el log cuando se realiza una accion cualquiera, en este caso para crear un usuario
        log = Log(
            id=str(ULID()),
            action="CREATE",
            entity_type="USER",
            entity_id=saved.id,
            description=f"User {saved.name} with Email {saved.email} created",
        )
        # llamas a save del repositorio de log
        await self._repo_log.save(log)

        return UserResponseDTO(
            id=saved.id,
            name=saved.name,
            email=saved.email,
            date_of_birth=saved.date_of_birth,
            bio=saved.bio,
            image_url=saved.image_url,
            status=saved.status,
            created_at=saved.created_at,
            updated_at=saved.updated_at,
        )
