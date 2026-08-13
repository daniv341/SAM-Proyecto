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

        return UserListResponseDTO(
            users=user_dtos,
            total=len(user_dtos),
            skip=skip,
            limit=limit,
        )
