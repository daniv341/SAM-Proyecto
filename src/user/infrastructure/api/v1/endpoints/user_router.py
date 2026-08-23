from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.user.application.ports.user_dtos import (
    CreateUserDTO,
    UpdateUserDTO,
    UserResponseDTO,
    UserListResponseDTO,
    LoginDTO,
    TokenResponseDTO,
    UserFilterDTO
)
from src.user.application.use_cases.create_user import CreateUserUseCase
from src.user.application.use_cases.get_user import GetUserUseCase
from src.user.application.use_cases.update_user import UpdateUserUseCase
from src.user.application.use_cases.delete_user import DeleteUserUseCase
from src.user.application.use_cases.login_user import LoginUserUseCase
from src.user.application.use_cases.logout_user import LogoutUserUseCase
from src.user.infrastructure.api.v1.dependencies import (
    get_create_user_use_case,
    get_get_user_use_case,
    get_update_user_use_case,
    get_delete_user_use_case,
    get_login_use_case,
    get_logout_use_case
)
from src.user.domain.user import UserStatus

# esta libreria hace que debas estar autenticado para acceder a un endpoint
from src.shared.config.auth_dependencies import CurrentUser

router = APIRouter(prefix="/users", tags=["Users"])


# AUTH
@router.post(
    "/auth/register",
    response_model=UserResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Crear/Registrar un nuevo user",
)
async def register(
    dto: CreateUserDTO,
    use_case: Annotated[CreateUserUseCase, Depends(get_create_user_use_case)],
) -> UserResponseDTO:
    return await use_case.execute(dto)


@router.post(
    "/auth/login", 
    response_model=TokenResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Iniciar sesión del user"
)
async def login(
    dto: LoginDTO, 
    use_case: Annotated[LoginUserUseCase, Depends(get_login_use_case)]
) -> TokenResponseDTO:
    return await use_case.execute(dto)


@router.post(
    "/auth/logout", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cerrar sesión del user"
)
async def logout(
    token: str,
    use_case: Annotated[LogoutUserUseCase, Depends(get_logout_use_case)],
    current_user: CurrentUser,
) -> None:
    return await use_case.execute(token)


@router.get(
    "/",
    response_model=UserListResponseDTO,
    summary="Listar todos los users",
)
async def list_users(
    use_case: Annotated[GetUserUseCase, Depends(get_get_user_use_case)],
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 20,
    status: UserStatus | None = None,
    created_at: datetime | None = None,
) -> UserListResponseDTO:
    filters = UserFilterDTO(
        status=status,
        created_at=created_at,
    )
    return await use_case.execute_all(filters, skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    response_model=UserResponseDTO,
    summary="Obtener un user por ID",
)
async def get_user(
    user_id: str,
    use_case: Annotated[GetUserUseCase, Depends(get_get_user_use_case)],
    current_user: CurrentUser, # con esta linea se asegura que el usuario esté autenticado para poder acceder al endpoint
) -> UserResponseDTO:
    return await use_case.execute_by_id(user_id)


@router.patch(
    "/{user_id}",
    response_model=UserResponseDTO,
    summary="Actualizar datos de un user",
)
async def update_user(
    user_id: str,
    dto: UpdateUserDTO,
    use_case: Annotated[UpdateUserUseCase, Depends(get_update_user_use_case)],
    current_user: CurrentUser,
) -> UserResponseDTO:
    return await use_case.execute(user_id, dto)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un user",
)
async def delete_user(
    user_id: str,
    use_case: Annotated[DeleteUserUseCase, Depends(get_delete_user_use_case)],
    current_user: CurrentUser,
) -> None:
    await use_case.execute(user_id)
