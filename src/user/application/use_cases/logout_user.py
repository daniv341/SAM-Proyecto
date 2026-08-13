from src.shared.config.security import revoke_token

class LogoutUserUseCase:
    async def execute(self, token: str) -> None:
        # revocamos el token de acceso para que ya no sea válido
        await revoke_token(token)