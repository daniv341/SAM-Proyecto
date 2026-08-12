from ulid import ULID

from src.user.application.ports.user_dtos import CreateUserDTO, UserResponseDTO
from src.user.domain.user import User
from src.user.domain.user_repository import UserRepository


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self._repo = user_repository

    async def execute(self, dto: CreateUserDTO) -> UserResponseDTO:
        user = User(
            id=str(ULID()),
            name=dto.name,
            date_of_birth=dto.date_of_birth,
            bio=dto.bio,
            image_url=dto.image_url,
        )

        saved = await self._repo.save(user)

        return UserResponseDTO(
            id=saved.id,
            name=saved.name,
            date_of_birth=saved.date_of_birth,
            bio=saved.bio,
            image_url=saved.image_url,
            status=saved.status,
            created_at=saved.created_at,
            updated_at=saved.updated_at,
        )
