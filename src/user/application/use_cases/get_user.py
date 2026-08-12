from src.user.application.ports.user_dtos import UserResponseDTO, UserListResponseDTO
from src.user.domain.user_repository import UserRepository
from src.shared.exceptions.domain_exceptions import EntityNotFoundException


class GetUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self._repo = user_repository

    async def execute_by_id(self, user_id: str) -> UserResponseDTO:
        user = await self._repo.find_by_id(user_id)
        if not user:
            raise EntityNotFoundException("User", user_id)

        return UserResponseDTO(
            id=user.id,
            name=user.name,
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
                id=item.id,
                name=item.name,
                date_of_birth=item.date_of_birth,
                status=item.status,
                bio=item.bio,
                image_url=item.image_url,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            for item in users
        ]

        return UserListResponseDTO(
            users=user_dtos,
            total=len(user_dtos),
            skip=skip,
            limit=limit,
        )
