from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.user.application.ports.user_dtos import (
    CreateUserDTO,
    UpdateUserDTO,
    UserResponseDTO,
    UserListResponseDTO,
)
from src.user.application.use_cases.create_user import CreateUserUseCase
from src.user.application.use_cases.get_user import GetUserUseCase
from src.user.application.use_cases.update_user import UpdateUserUseCase
from src.user.application.use_cases.delete_user import DeleteUserUseCase
from src.user.infrastructure.api.v1.dependencies import (
    get_create_user_use_case,
    get_get_user_use_case,
    get_update_user_use_case,
    get_delete_user_use_case,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=UserResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo user",
)
async def create_user(
    dto: CreateUserDTO,
    use_case: Annotated[CreateUserUseCase, Depends(get_create_user_use_case)],
) -> UserResponseDTO:
    return await use_case.execute(dto)


@router.get(
    "/",
    response_model=UserListResponseDTO,
    summary="Listar todos los users",
)
async def list_users(
    use_case: Annotated[GetUserUseCase, Depends(get_get_user_use_case)],
    skip: int = 0,
    limit: int = 20,
) -> UserListResponseDTO:
    return await use_case.execute_all(skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    response_model=UserResponseDTO,
    summary="Obtener un user por ID",
)
async def get_user(
    user_id: str,
    use_case: Annotated[GetUserUseCase, Depends(get_get_user_use_case)],
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
) -> None:
    await use_case.execute(user_id)
