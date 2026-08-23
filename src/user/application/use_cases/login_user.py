from ulid import ULID
from src.shared.exceptions.domain_exceptions import DomainException

from src.user.domain.user_repository import UserRepository
from src.user.application.ports.user_dtos import LoginDTO, TokenResponseDTO
from src.shared.exceptions.domain_exceptions import EntityNotFoundException, InvalidValueException
from src.shared.config.security import verify_password, create_access_token
from src.user.domain.user import UserStatus

from src.log.domain.log import Log
from src.log.domain.log_repository import LogRepository

class LoginUserUseCase:
    def __init__(self, user_repository: UserRepository, log_repository: LogRepository):
        self._repo = user_repository
        self._repo_log = log_repository

    async def execute(self, dto: LoginDTO) -> TokenResponseDTO:
        user = await self._repo.find_by_email(dto.email)

        if not user:
            raise EntityNotFoundException("User", dto.email)

        if user.status != UserStatus.ACTIVE:
            raise DomainException("Un user que no este ACTIVE no puede ingresar al sistema")
        
        # verificamos la contraseña
        if not verify_password(dto.password, user.password):
            raise InvalidValueException("credenciales inválidas, vuelva a intentar")

        # si la contraseña es correcta, generamos un token de acceso y lo retornamos
        token = create_access_token({"sub": user.id, "email": user.email})

        log = Log(
            id=str(ULID()),
            action="LOGIN",
            entity_type="USER",
            entity_id=user.id,
            description=f"User {user.name} with Email {user.email} login"
        )
        # llamas a save del repositorio de log
        await self._repo_log.save(log) 

        return TokenResponseDTO(access_token=token)