from ulid import ULID

from src.shared.config.security import hash_password
from src.user.application.ports.user_dtos import UpdateUserDTO, UserResponseDTO
from src.user.domain.user_repository import UserRepository
from src.shared.exceptions.domain_exceptions import EntityNotFoundException

from src.log.domain.log import Log
from src.log.domain.log_repository import LogRepository

class UpdateUserUseCase:
    def __init__(self, user_repository: UserRepository, log_repository: LogRepository):
        self._repo = user_repository
        self._repo_log = log_repository

    async def execute(self, user_id: str, dto: UpdateUserDTO) -> UserResponseDTO:
        user = await self._repo.find_by_id(user_id)
        if not user:
            raise EntityNotFoundException("User", user_id)

        if dto.password is not None:
            user.password = hash_password(dto.password)
        if dto.status is not None:
            user.banned_changed_to_suspended(dto.status)
            user.status = dto.status
        if dto.bio is not None:
            user.bio = dto.bio
        if dto.image_url is not None:
            user.image_url = dto.image_url

        user._touch()
        updated = await self._repo.update(user)

        log = Log(
            id=str(ULID()),
            action="UPDATE",
            entity_type="USER",
            entity_id=user.id,
            description=f"User {user.name} with Email {user.email} updated",
            created_at=updated.created_at
        )
        # llamas a save del repositorio de log
        await self._repo_log.save(log) 

        return UserResponseDTO(
            id=updated.id,
            name=updated.name,
            email=updated.email,
            date_of_birth=updated.date_of_birth,
            status=updated.status,
            bio=updated.bio,
            image_url=updated.image_url,
            created_at=updated.created_at,
            updated_at=updated.updated_at,
        )
