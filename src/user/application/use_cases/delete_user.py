from ulid import ULID

from src.user.domain.user_repository import UserRepository
from src.shared.exceptions.domain_exceptions import EntityNotFoundException

from src.log.domain.log import Log
from src.log.domain.log_repository import LogRepository

class DeleteUserUseCase:
    def __init__(self, user_repository: UserRepository, log_repository: LogRepository):
        self._repo = user_repository
        self._repo_log = log_repository

    async def execute(self, user_id: str) -> None:
        user = await self._repo.find_by_id(user_id)
        if not user:
            raise EntityNotFoundException("User", user_id)

        await self._repo.delete(user_id)

        log = Log(
            id=str(ULID()),
            action="DELETE",
            entity_type="USER",
            entity_id=user.id,
            description=f"User {user.name} with Email {user.email} deleted"
        )
        # llamas a save del repositorio de log
        await self._repo_log.save(log)        
