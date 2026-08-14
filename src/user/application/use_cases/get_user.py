from ulid import ULID

from src.user.application.ports.user_dtos import UserResponseDTO, UserListResponseDTO
from src.user.domain.user_repository import UserRepository
from src.shared.exceptions.domain_exceptions import EntityNotFoundException

from src.log.domain.log import Log
from src.log.domain.log_repository import LogRepository

class GetUserUseCase:
    def __init__(self, user_repository: UserRepository, log_repository: LogRepository):
        self._repo = user_repository
        self._repo_log = log_repository

    async def execute_by_id(self, user_id: str) -> UserResponseDTO:
        user = await self._repo.find_by_id(user_id)
        if not user:
            raise EntityNotFoundException("User", user_id)

        log = Log(
            id=str(ULID()),
            action="GET",
            entity_type="USER",
            entity_id=user.id,
            description=f"User {user.name} with Email {user.email} get"
        )
        # llamas a save del repositorio de log
        await self._repo_log.save(log) 

        return UserResponseDTO(
            id=user.id,
            name=user.name,
            email=user.email,
            date_of_birth=user.date_of_birth,
            status=user.status,
            bio=user.bio,
            image_url=user.image_url,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    async def execute_all(self, skip: int = 0, limit: int = 20) -> UserListResponseDTO:
        users = await self._repo.find_all(skip=skip, limit=limit)

        user_dtos = [
            UserResponseDTO(
                id=u.id,
                name=u.name,
                email=u.email,
                date_of_birth=u.date_of_birth,
                status=u.status,
                bio=u.bio,
                image_url=u.image_url,
                created_at=u.created_at,
                updated_at=u.updated_at,
            )
            for u in users
        ]

        log = Log(
            id=str(ULID()),
            action="GETALL",
            entity_type="USER",
            entity_id="None",
            description=f"Get All ejecuted"
        )
        # llamas a save del repositorio de log
        await self._repo_log.save(log) 

        return UserListResponseDTO(
            users=user_dtos,
            total=len(user_dtos),
            skip=skip,
            limit=limit,
        )
