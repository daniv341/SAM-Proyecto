from src.user.domain.user_repository import UserRepository
from src.shared.exceptions.domain_exceptions import EntityNotFoundException


class DeleteUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self._repo = user_repository

    async def execute(self, user_id: str) -> None:
        user = await self._repo.find_by_id(user_id)
        if not user:
            raise EntityNotFoundException("User", user_id)

        await self._repo.delete(user_id)
