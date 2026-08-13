from src.user.domain.user_repository import UserRepository
from src.user.application.ports.user_dtos import LoginDTO, TokenResponseDTO
from src.shared.exceptions.domain_exceptions import EntityNotFoundException, InvalidValueException
from src.shared.config.security import verify_password, create_access_token

class LoginUserUseCase:
    def __init__(self, repo: UserRepository):
        self._repo = repo

    async def execute(self, dto: LoginDTO) -> TokenResponseDTO:
        user = await self._repo.find_by_email(dto.email)
        if not user:
            raise EntityNotFoundException("User", dto.email)
        # verificamos la contraseña
        if not verify_password(dto.password, user.password):
            raise InvalidValueException("credenciales inválidas, vuelva a intentar")

        # si la contraseña es correcta, generamos un token de acceso y lo retornamos
        token = create_access_token({"sub": user.id, "email": user.email})
        return TokenResponseDTO(access_token=token)