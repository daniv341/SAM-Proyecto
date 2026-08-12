from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt, JWTError
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.shared.config.settings import settings

# esquema de seguridad para obtener el token de acceso de la cabecera Authorization
bearer_scheme = HTTPBearer()

# En producción reemplazar por Redis
# En memoria para almacenar tokens revocados
_token_blacklist: set[str] = set()


# función para obtener el token de acceso de la cabecera Authorization
def hash_password(plain: str) -> str:
    salt = bcrypt.gensalt() # generamos un salt aleatorio
    hashed = bcrypt.hashpw(plain.encode("utf-8"), salt) # hasheamos la contraseña con el salt
    return hashed.decode("utf-8") # retornamos el hash como string

# verificamos si la contraseña ingresada coincide con el hash en la bd
def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(
        plain.encode("utf-8"), # convertimos la contraseña ingresada a bytes
        hashed.encode("utf-8") # convertimos el hash de la bd a bytes
    )

# función para obtener el token de acceso de la cabecera Authorization
def create_access_token(data: dict) -> str:
    # copiamos el diccionario para no modificar el original
    payload = data.copy() 
    # agregamos la fecha de expiración al payload
    payload["exp"] = datetime.now(timezone.utc) + timedelta(
        # la expiración del token se define en settings.py
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    # retorna el token de acceso generado con el payload y la clave secreta
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# función para revocar un token de acceso, agregándolo a la lista negra
async def revoke_token(token: str) -> None:
    _token_blacklist.add(token)

# función para decodificar un token de acceso y verificar si está revocado
def decode_token(token: str) -> dict:
    # si esta en la lista negra lanza el error 401
    if token in _token_blacklist:
        raise HTTPException(status_code=401,detail="Token revocado")

    # intentamos decodificar el token con la clave secreta y el algoritmo definido en settings.py
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
    # si el token es inválido o expirado lanza el error 401
    except JWTError:
        raise HTTPException(status_code=401,detail="Token inválido o expirado")

    return payload