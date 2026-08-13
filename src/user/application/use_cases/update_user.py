from src.shared.config.security import hash_password
from src.user.application.ports.user_dtos import UpdateUserDTO, UserResponseDTO
from src.user.domain.user_repository import UserRepository
from src.shared.exceptions.domain_exceptions import EntityNotFoundException


class UpdateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self._repo = user_repository

    async def execute(self, user_id: str, dto: UpdateUserDTO) -> UserResponseDTO:
        user = await self._repo.find_by_id(user_id)
        if not user:
            raise EntityNotFoundException("User", user_id)

        if dto.password is not None:
            user.name = hash_password(dto.password)
        if dto.status is not None:
            user.banned_changed_to_suspended(dto.status)
            user.status = dto.status
        if dto.bio is not None:
            user.bio = dto.bio
        if dto.image_url is not None:
            user.image_url = dto.image_url

        user._touch()
        updated = await self._repo.update(user)

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
