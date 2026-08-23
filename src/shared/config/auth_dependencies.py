from typing import Annotated

from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.shared.config.security import decode_token
from src.user.infrastructure.api.v1.dependencies import UserRepoDep
from src.user.domain.user import User, Role

# esquema de seguridad para obtener el token de acceso de la cabecera Authorization
bearer_scheme = HTTPBearer()

# función para obtener el usuario actual a partir del token de acceso
async def get_current_user(
    repo: UserRepoDep,
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
) -> User:

    # obtenemos el token de acceso de la cabecera Authorization
    token = credentials.credentials

    # decodificamos el token de acceso y obtenemos el payload
    payload = decode_token(token)

    # obtenemos el id del usuario del payload
    user_id = payload.get("sub")

    # si el id del usuario no está en el payload, lanzamos un error 401, por mas que el token sea válido, no se puede obtener el usuario
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    # buscamos el usuario en la base de datos a partir del id obtenido del payload
    user = await repo.find_by_id(user_id)

    # si el usuario no existe, lanzamos un error 401, por mas que el token sea válido, no se puede obtener el usuario
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Usuario no encontrado"
        )

    # retornamos el usuario actual
    return user

# CurrentUser es un alias para User que se obtiene del token y depende de get_current_user
CurrentUser = Annotated[User, Depends(get_current_user)]


async def require_admin(
    current_user: CurrentUser,
) -> User:

    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Administrator permissions required",
        )

    return current_user


CurrentAdmin = Annotated[User, Depends(require_admin)]