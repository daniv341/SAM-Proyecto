#!/usr/bin/env python3
"""
Generador de estructura de objeto de dominio
Proyecto: eSports Championship Backend
Arquitectura: Hexagonal (ports & adapters)

Uso:
    python create_object.py
    python create_object.py --name tournament
    python create_object.py --name tournament --base-path src
"""

import argparse
import sys
from pathlib import Path


# ──────────────────────────────────────────────
# Helpers de nombrado
# ──────────────────────────────────────────────

def to_pascal(snake: str) -> str:
    """tournament_registration → TournamentRegistration"""
    return "".join(word.capitalize() for word in snake.split("_"))

def to_snake(name: str) -> str:
    """Normaliza a snake_case y valida que sea un identificador válido."""
    name = name.strip().lower().replace("-", "_").replace(" ", "_")
    if not name.isidentifier():
        raise ValueError(f"'{name}' no es un nombre válido para un objeto de dominio.")
    return name

def to_plural(snake: str) -> str:
    """Heurística simple para plural en rutas REST."""
    if snake.endswith("y"):
        return snake[:-1] + "ies"
    if snake.endswith(("s", "sh", "ch", "x", "z")):
        return snake + "es"
    return snake + "s"


# ──────────────────────────────────────────────
# Plantillas de contenido
# ──────────────────────────────────────────────

def tpl_domain_entity(obj: str, pascal: str) -> str:
    return f'''\
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

from src.shared.exceptions.domain_exceptions import InvalidValueException


class {pascal}Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


@dataclass
class {pascal}:
    """
    Entidad de dominio {pascal}.
    No tiene dependencias de frameworks externos.
    """
    id: str
    name: str
    status: {pascal}Status = {pascal}Status.ACTIVE
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if not self.name or len(self.name.strip()) < 2:
            raise InvalidValueException("El nombre debe tener al menos 2 caracteres.")

    def activate(self) -> None:
        self.status = {pascal}Status.ACTIVE
        self._touch()

    def deactivate(self) -> None:
        self.status = {pascal}Status.INACTIVE
        self._touch()

    def _touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc)
'''


def tpl_domain_repository(obj: str, pascal: str) -> str:
    return f'''\
from abc import ABC, abstractmethod

from src.{obj}.domain.{obj} import {pascal}


class {pascal}Repository(ABC):
    """
    Puerto de salida (driven port).
    Define el contrato que cualquier implementación de repositorio debe cumplir.
    """

    @abstractmethod
    async def save(self, {obj}: {pascal}) -> {pascal}:
        """Persiste un nuevo {obj}."""
        ...

    @abstractmethod
    async def find_by_id(self, {obj}_id: str) -> {pascal} | None:
        """Busca un {obj} por su ID."""
        ...

    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 20) -> list[{pascal}]:
        """Devuelve una lista paginada de {obj}s."""
        ...

    @abstractmethod
    async def update(self, {obj}: {pascal}) -> {pascal}:
        """Actualiza un {obj} existente."""
        ...

    @abstractmethod
    async def delete(self, {obj}_id: str) -> None:
        """Elimina un {obj} por su ID."""
        ...
'''


def tpl_dtos(obj: str, pascal: str) -> str:
    return f'''\
from datetime import datetime
from pydantic import BaseModel

from src.{obj}.domain.{obj} import {pascal}Status


class Create{pascal}DTO(BaseModel):
    name: str


class Update{pascal}DTO(BaseModel):
    name: str | None = None


class {pascal}ResponseDTO(BaseModel):
    id: str
    name: str
    status: {pascal}Status
    created_at: datetime
    updated_at: datetime

    model_config = {{"from_attributes": True}}


class {pascal}ListResponseDTO(BaseModel):
    items: list[{pascal}ResponseDTO]
    total: int
    skip: int
    limit: int
'''


def tpl_create_use_case(obj: str, pascal: str) -> str:
    return f'''\
from ulid import ULID

from src.{obj}.application.ports.{obj}_dtos import Create{pascal}DTO, {pascal}ResponseDTO
from src.{obj}.domain.{obj} import {pascal}
from src.{obj}.domain.{obj}_repository import {pascal}Repository


class Create{pascal}UseCase:
    def __init__(self, {obj}_repository: {pascal}Repository):
        self._repo = {obj}_repository

    async def execute(self, dto: Create{pascal}DTO) -> {pascal}ResponseDTO:
        {obj} = {pascal}(
            id=str(ULID()),
            name=dto.name,
        )

        saved = await self._repo.save({obj})

        return {pascal}ResponseDTO(
            id=saved.id,
            name=saved.name,
            status=saved.status,
            created_at=saved.created_at,
            updated_at=saved.updated_at,
        )
'''


def tpl_get_use_case(obj: str, pascal: str) -> str:
    return f'''\
from src.{obj}.application.ports.{obj}_dtos import {pascal}ResponseDTO, {pascal}ListResponseDTO
from src.{obj}.domain.{obj}_repository import {pascal}Repository
from src.shared.exceptions.domain_exceptions import EntityNotFoundException


class Get{pascal}UseCase:
    def __init__(self, {obj}_repository: {pascal}Repository):
        self._repo = {obj}_repository

    async def execute_by_id(self, {obj}_id: str) -> {pascal}ResponseDTO:
        {obj} = await self._repo.find_by_id({obj}_id)
        if not {obj}:
            raise EntityNotFoundException("{pascal}", {obj}_id)

        return {pascal}ResponseDTO(
            id={obj}.id,
            name={obj}.name,
            status={obj}.status,
            created_at={obj}.created_at,
            updated_at={obj}.updated_at,
        )

    async def execute_all(self, skip: int = 0, limit: int = 20) -> {pascal}ListResponseDTO:
        items = await self._repo.find_all(skip=skip, limit=limit)

        item_dtos = [
            {pascal}ResponseDTO(
                id=item.id,
                name=item.name,
                status=item.status,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            for item in items
        ]

        return {pascal}ListResponseDTO(
            items=item_dtos,
            total=len(item_dtos),
            skip=skip,
            limit=limit,
        )
'''


def tpl_update_use_case(obj: str, pascal: str) -> str:
    return f'''\
from src.{obj}.application.ports.{obj}_dtos import Update{pascal}DTO, {pascal}ResponseDTO
from src.{obj}.domain.{obj}_repository import {pascal}Repository
from src.shared.exceptions.domain_exceptions import EntityNotFoundException


class Update{pascal}UseCase:
    def __init__(self, {obj}_repository: {pascal}Repository):
        self._repo = {obj}_repository

    async def execute(self, {obj}_id: str, dto: Update{pascal}DTO) -> {pascal}ResponseDTO:
        {obj} = await self._repo.find_by_id({obj}_id)
        if not {obj}:
            raise EntityNotFoundException("{pascal}", {obj}_id)

        if dto.name is not None:
            {obj}.name = dto.name

        {obj}._touch()
        updated = await self._repo.update({obj})

        return {pascal}ResponseDTO(
            id=updated.id,
            name=updated.name,
            status=updated.status,
            created_at=updated.created_at,
            updated_at=updated.updated_at,
        )
'''


def tpl_delete_use_case(obj: str, pascal: str) -> str:
    return f'''\
from src.{obj}.domain.{obj}_repository import {pascal}Repository
from src.shared.exceptions.domain_exceptions import EntityNotFoundException


class Delete{pascal}UseCase:
    def __init__(self, {obj}_repository: {pascal}Repository):
        self._repo = {obj}_repository

    async def execute(self, {obj}_id: str) -> None:
        {obj} = await self._repo.find_by_id({obj}_id)
        if not {obj}:
            raise EntityNotFoundException("{pascal}", {obj}_id)

        await self._repo.delete({obj}_id)
'''


def tpl_model(obj: str, pascal: str) -> str:
    return f'''\
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Column, DateTime

from sqlmodel import SQLModel, Field

from src.{obj}.domain.{obj} import {pascal}Status


class {pascal}Model(SQLModel, table=True):
    """
    Modelo de base de datos para {pascal}.
    Pertenece a la capa de infraestructura, separado de la entidad de dominio.
    """
    __tablename__ = "{to_plural(obj)}"

    id: str = Field(primary_key=True)
    name: str = Field(max_length=100, index=True)
    status: {pascal}Status = Field(default={pascal}Status.ACTIVE)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
'''


def tpl_mapper(obj: str, pascal: str) -> str:
    return f'''\
from src.{obj}.domain.{obj} import {pascal}
from src.{obj}.infrastructure.repositories.{obj}_model import {pascal}Model


class {pascal}Mapper:
    """Convierte entre la entidad de dominio y el modelo de persistencia."""

    @staticmethod
    def to_domain(model: {pascal}Model) -> {pascal}:
        return {pascal}(
            id=model.id,
            name=model.name,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model({obj}: {pascal}) -> {pascal}Model:
        return {pascal}Model(
            id={obj}.id,
            name={obj}.name,
            status={obj}.status,
            created_at={obj}.created_at,
            updated_at={obj}.updated_at,
        )
'''


def tpl_sqlalchemy_repo(obj: str, pascal: str) -> str:
    return f'''\
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.{obj}.domain.{obj} import {pascal}
from src.{obj}.domain.{obj}_repository import {pascal}Repository
from src.{obj}.infrastructure.repositories.{obj}_mapper import {pascal}Mapper
from src.{obj}.infrastructure.repositories.{obj}_model import {pascal}Model


class SQLAlchemy{pascal}Repository({pascal}Repository):
    """
    Adaptador de salida (driven adapter).
    Implementación concreta del repositorio usando SQLAlchemy + SQLModel.
    """

    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, {obj}: {pascal}) -> {pascal}:
        model = {pascal}Mapper.to_model({obj})
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return {pascal}Mapper.to_domain(model)

    async def find_by_id(self, {obj}_id: str) -> {pascal} | None:
        result = await self._session.execute(
            select({pascal}Model).where({pascal}Model.id == {obj}_id)
        )
        model = result.scalar_one_or_none()
        return {pascal}Mapper.to_domain(model) if model else None

    async def find_all(self, skip: int = 0, limit: int = 20) -> list[{pascal}]:
        result = await self._session.execute(
            select({pascal}Model).offset(skip).limit(limit)
        )
        models = result.scalars().all()
        return [{pascal}Mapper.to_domain(m) for m in models]

    async def update(self, {obj}: {pascal}) -> {pascal}:
        result = await self._session.execute(
            select({pascal}Model).where({pascal}Model.id == {obj}.id)
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"{pascal}Model con id \\"{{{obj}.id}}\\" no encontrado.")

        model.name = {obj}.name
        model.status = {obj}.status
        model.updated_at = {obj}.updated_at

        await self._session.flush()
        await self._session.refresh(model)
        return {pascal}Mapper.to_domain(model)

    async def delete(self, {obj}_id: str) -> None:
        result = await self._session.execute(
            select({pascal}Model).where({pascal}Model.id == {obj}_id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()
'''


def tpl_dependencies(obj: str, pascal: str) -> str:
    return f'''\
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.database.engine import get_session
from src.{obj}.infrastructure.repositories.sqlalchemy_{obj}_repository import SQLAlchemy{pascal}Repository
from src.{obj}.application.use_cases.create_{obj} import Create{pascal}UseCase
from src.{obj}.application.use_cases.get_{obj} import Get{pascal}UseCase
from src.{obj}.application.use_cases.update_{obj} import Update{pascal}UseCase
from src.{obj}.application.use_cases.delete_{obj} import Delete{pascal}UseCase

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_{obj}_repository(session: SessionDep) -> SQLAlchemy{pascal}Repository:
    return SQLAlchemy{pascal}Repository(session)


{pascal}RepoDep = Annotated[SQLAlchemy{pascal}Repository, Depends(get_{obj}_repository)]


def get_create_{obj}_use_case(repo: {pascal}RepoDep) -> Create{pascal}UseCase:
    return Create{pascal}UseCase(repo)


def get_get_{obj}_use_case(repo: {pascal}RepoDep) -> Get{pascal}UseCase:
    return Get{pascal}UseCase(repo)


def get_update_{obj}_use_case(repo: {pascal}RepoDep) -> Update{pascal}UseCase:
    return Update{pascal}UseCase(repo)


def get_delete_{obj}_use_case(repo: {pascal}RepoDep) -> Delete{pascal}UseCase:
    return Delete{pascal}UseCase(repo)
'''


def tpl_router(obj: str, pascal: str) -> str:
    plural = to_plural(obj)
    plural_pascal = to_pascal(plural)
    return f'''\
from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.{obj}.application.ports.{obj}_dtos import (
    Create{pascal}DTO,
    Update{pascal}DTO,
    {pascal}ResponseDTO,
    {pascal}ListResponseDTO,
)
from src.{obj}.application.use_cases.create_{obj} import Create{pascal}UseCase
from src.{obj}.application.use_cases.get_{obj} import Get{pascal}UseCase
from src.{obj}.application.use_cases.update_{obj} import Update{pascal}UseCase
from src.{obj}.application.use_cases.delete_{obj} import Delete{pascal}UseCase
from src.{obj}.infrastructure.api.v1.dependencies import (
    get_create_{obj}_use_case,
    get_get_{obj}_use_case,
    get_update_{obj}_use_case,
    get_delete_{obj}_use_case,
)

router = APIRouter(prefix="/{plural}", tags=["{plural_pascal}"])


@router.post(
    "/",
    response_model={pascal}ResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo {obj}",
)
async def create_{obj}(
    dto: Create{pascal}DTO,
    use_case: Annotated[Create{pascal}UseCase, Depends(get_create_{obj}_use_case)],
) -> {pascal}ResponseDTO:
    return await use_case.execute(dto)


@router.get(
    "/",
    response_model={pascal}ListResponseDTO,
    summary="Listar todos los {plural}",
)
async def list_{plural}(
    use_case: Annotated[Get{pascal}UseCase, Depends(get_get_{obj}_use_case)],
    skip: int = 0,
    limit: int = 20,
) -> {pascal}ListResponseDTO:
    return await use_case.execute_all(skip=skip, limit=limit)


@router.get(
    "/{{{obj}_id}}",
    response_model={pascal}ResponseDTO,
    summary="Obtener un {obj} por ID",
)
async def get_{obj}(
    {obj}_id: str,
    use_case: Annotated[Get{pascal}UseCase, Depends(get_get_{obj}_use_case)],
) -> {pascal}ResponseDTO:
    return await use_case.execute_by_id({obj}_id)


@router.patch(
    "/{{{obj}_id}}",
    response_model={pascal}ResponseDTO,
    summary="Actualizar datos de un {obj}",
)
async def update_{obj}(
    {obj}_id: str,
    dto: Update{pascal}DTO,
    use_case: Annotated[Update{pascal}UseCase, Depends(get_update_{obj}_use_case)],
) -> {pascal}ResponseDTO:
    return await use_case.execute({obj}_id, dto)


@router.delete(
    "/{{{obj}_id}}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un {obj}",
)
async def delete_{obj}(
    {obj}_id: str,
    use_case: Annotated[Delete{pascal}UseCase, Depends(get_delete_{obj}_use_case)],
) -> None:
    await use_case.execute({obj}_id)
'''


def tpl_test_domain(obj: str, pascal: str) -> str:
    return f'''\
import pytest
from datetime import datetime, timezone

from src.{obj}.domain.{obj} import {pascal}, {pascal}Status
from src.shared.exceptions.domain_exceptions import InvalidValueException


def make_{obj}(**overrides) -> {pascal}:
    """Factory con valores válidos por defecto para tests."""
    defaults = dict(
        id="01JTEST00000000000000000001",
        name="Test {pascal}",
        status={pascal}Status.ACTIVE,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    defaults.update(overrides)
    return {pascal}(**defaults)


class TestCreate{pascal}:
    def test_create_valid(self):
        {obj} = make_{obj}()
        assert {obj}.name == "Test {pascal}"
        assert {obj}.status == {pascal}Status.ACTIVE

class TestName:
    def test_invalid_name(self):
        with pytest.raises(InvalidValueException):
            Name("a")

    def test_valid_name(self):
        name = Name("nombre")
        assert name.value == "nombre"

class TestStatus:
    def test_ban_{obj}(self):
        status = {pascal}Status.BANNED
        assert status.value == {pascal}Status.BANNED

    def test_active_{obj}(self):
        status = {pascal}Status.ACTIVE
        assert status.value == {pascal}Status.ACTIVE

    def test_cannot_suspend_banned_{obj}(self):
        {obj} = make_{obj}(status={pascal}Status.BANNED)
        with pytest.raises(InvalidValueException):
            {obj}.banned_changed_to_suspended({pascal}Status.SUSPENDED)
        assert {obj}.status == {pascal}Status.BANNED
'''


def tpl_alembic_hint(obj: str, pascal: str) -> str:
    return f"""\
# ─────────────────────────────────────────────────────────────
# RECORDATORIO: registrar {pascal}Model en alembic/env.py
# ─────────────────────────────────────────────────────────────
# Agregar esta línea junto a los demás imports de modelos:
#
#   from src.{obj}.infrastructure.repositories.{obj}_model import {pascal}Model  # noqa: F401
#
# Luego ejecutar:
#   alembic revision --autogenerate -m "create {to_plural(obj)} table"
#   alembic upgrade head
# ─────────────────────────────────────────────────────────────
"""


def tpl_main_hint(obj: str, pascal: str) -> str:
    plural = to_plural(obj)
    return f"""\
# ─────────────────────────────────────────────────────────────
# RECORDATORIO: registrar el router en src/main.py
# ─────────────────────────────────────────────────────────────
# 1. Importar el router:
#
#   from src.{obj}.infrastructure.api.v1.endpoints.{obj}_router import router as {obj}_router
#
# 2. Registrarlo (junto a los demás routers):
#
#   app.include_router({obj}_router, prefix=API_PREFIX)
# ─────────────────────────────────────────────────────────────
"""


def tpl_validator(obj: str, pascal: str) -> str:
    return f'''\
"""
Funciones auxiliares de validación para {pascal}.

Propósito: centralizar las validaciones de unicidad, existencia de FKs
y construcción del ResponseDTO enriquecido con datos de objetos relacionados.
Estas funciones son llamadas desde los casos de uso (create, update, get).

── Cómo extender este archivo ────────────────────────────────────────────────
1. Agrega el repositorio de cada objeto relacionado como parámetro de la función.
2. En _to_{obj}_unicity   → verifica que campos únicos no estén ya en uso.
3. En _to_{obj}_validator → verifica que cada FK exista antes de crear.
4. En _to_update_{obj}_validator → igual que el anterior pero sin chequear
   campos que no se pueden cambiar en un update (ej: user_id).
5. En _to_{obj}_response  → carga los objetos relacionados y construye el DTO
   con sus respectivos sub-DTOs (ej: GameResponseShortDTO, RegionResponseShortDTO).
──────────────────────────────────────────────────────────────────────────────
"""
from src.{obj}.domain.{obj} import {pascal}
from src.{obj}.domain.{obj}_repository import {pascal}Repository
from src.{obj}.application.ports.{obj}_dtos import {pascal}ResponseDTO
from src.shared.exceptions.domain_exceptions import (
    EntityNotFoundException,
    EntityAlreadyExistsException,
)

# TODO: importar los repositorios de los objetos relacionados, por ejemplo:
# from src.<related>.domain.<related>_repository import <Related>Repository

# TODO: importar los sub-DTOs de los objetos relacionados, por ejemplo:
# from src.<related>.application.ports.<related>_dtos import <Related>ResponseShortDTO


async def _to_{obj}_unicity(
    {obj}: {pascal},
    {obj}_repository: {pascal}Repository,
) -> None:
    """
    Verifica que los campos únicos del {obj} no estén ya registrados.
    Lanza EntityAlreadyExistsException si encuentra un duplicado.

    TODO: agregar una verificación por cada campo único del objeto, por ejemplo:

        existing = await {obj}_repository.find_by_name({obj}.name)
        if existing:
            raise EntityAlreadyExistsException("{pascal}", "name", {obj}.name)
    """
    pass


async def _to_{obj}_validator(
    {obj}: {pascal},
    # TODO: agregar los repositorios de FKs como parámetros, por ejemplo:
    # related_repository: RelatedRepository,
) -> None:
    """
    Verifica que todos los objetos referenciados por FKs existan en la BD.
    Úsala en el caso de uso de creación antes de llamar a repo.save().
    Lanza EntityNotFoundException si alguna FK no existe.

    TODO: agregar una verificación por cada FK del objeto, por ejemplo:

        related = await related_repository.find_by_id({obj}.related_id)
        if not related:
            raise EntityNotFoundException("Related", {obj}.related_id)
    """
    pass


async def _to_update_{obj}_validator(
    {obj}: {pascal},
    # TODO: agregar los repositorios de FKs actualizables como parámetros.
    # Generalmente son los mismos que _to_{obj}_validator, excepto los campos
    # que no se pueden cambiar en un update (ej: user_id, owner_id).
) -> None:
    """
    Igual que _to_{obj}_validator pero aplicado al flujo de actualización.
    Solo valida las FKs que se permiten modificar.

    TODO: agregar verificaciones para cada FK que sea editable, por ejemplo:

        if {obj}.related_id:
            related = await related_repository.find_by_id({obj}.related_id)
            if not related:
                raise EntityNotFoundException("Related", {obj}.related_id)
    """
    pass


async def _to_{obj}_response(
    {obj}: {pascal},
    # TODO: agregar los repositorios necesarios para cargar los datos relacionados.
) -> {pascal}ResponseDTO:
    """
    Construye el {pascal}ResponseDTO cargando los datos de los objetos
    relacionados. Úsala al final de los casos de uso create, update y get
    en lugar de construir el DTO directamente.

    TODO: cargar cada objeto relacionado y pasarlo como sub-DTO al ResponseDTO.
    Ejemplo:

        related = await related_repository.find_by_id({obj}.related_id)
        if not related:
            raise EntityNotFoundException("Related", {obj}.related_id)

        return {pascal}ResponseDTO(
            id={obj}.id,
            name={obj}.name,
            status={obj}.status,
            related=RelatedResponseShortDTO(field=related.field),
            created_at={obj}.created_at,
            updated_at={obj}.updated_at,
        )
    """
    # Implementación base sin relaciones (reemplazar con la versión completa)
    return {pascal}ResponseDTO(
        id={obj}.id,
        name={obj}.name,
        status={obj}.status,
        created_at={obj}.created_at,
        updated_at={obj}.updated_at,
    )
'''


def tpl_test_endpoint(obj: str, pascal: str) -> str:
    plural = to_plural(obj)
    plural_title = plural.replace("_", " ").title().replace(" ", "")
    return f'''\
"""
Tests de integración para los endpoints de {pascal}.
Usa TestClient de FastAPI contra la app real (sin mocks).

Fixtures:
  client          → cliente HTTP reutilizable por sesión de test.
  {obj}_payload   → payload mínimo válido para POST.
  created_{obj}   → crea un {obj} en la BD y devuelve la respuesta JSON.

Cómo extender:
  - Agrega IDs de objetos relacionados (ej: GAME_IDS, REGION_IDS) como listas
    y funciones random_*_id() siguiendo el mismo patrón.
  - Actualiza {obj}_payload con los campos FK correspondientes.
  - Agrega nuevos métodos en las clases de test existentes o crea clases nuevas.
"""
import uuid
import pytest
from fastapi.testclient import TestClient

from src.main import app

# TODO: si el objeto tiene FKs, agregar listas de IDs válidos y funciones
# random_*_id() para usarlas en los payloads, por ejemplo:
#
# RELATED_IDS = ["01ABC...", "01DEF..."]
#
# def random_related_id() -> str:
#     import random
#     return random.choice(RELATED_IDS)


@pytest.fixture 
def client(): 
    with TestClient(app) as c: 
        yield c


@pytest.fixture
def {obj}_payload() -> dict:
    """Payload mínimo válido para crear un {obj}."""
    return {{
        "name": f"test_{obj}_{{uuid.uuid4().hex[:8]}}",
        # TODO: agregar aquí los campos FK y opcionales del objeto, por ejemplo:
        # "related_id": random_related_id(),
        # "description": "descripción de prueba",
    }}


@pytest.fixture
def created_{obj}({obj}_payload, client) -> dict:
    """Crea un user real en la BD y devuelve la respuesta; útil como precondición."""
    response = client.post("/api/v1/{plural}/", json={obj}_payload)
    assert response.status_code == 201, f"Setup falló: {{response.text}}"
    return response.json()


class TestCreate{pascal}:
    # prueba el endpoint de post con todos los atributos
    def test_create_{obj}_success(self, {obj}_payload, client):
        response = client.post("/api/v1/{plural}/", json={obj}_payload)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == {obj}_payload["name"]
        assert data["status"] == "ACTIVE"
        assert "id" in data

    # prueba el endpoint de post sin los atributos opcionales
    def test_create_{obj}_without_optional_fields(self, client):
        payload = {{
            "name": "name",
        }}
        response = client.post("/api/v1/{plural}/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "ACTIVE"
        assert data["name"] == payload["name"]

    # prueba el endpoint de post sin el name, lanza error
    def test_create_{obj}_missing_required_field(self, {obj}_payload, client):
        payload = {obj}_payload.copy()
        del payload["name"]
        response = client.post("/api/v1/{plural}/", json=payload)
        assert response.status_code == 422   # Unprocessable Entity

    # prueba el endpoint de post con date_of_birth invalido, lanza error
    def test_create_{obj}_invalid_date_format(self, {obj}_payload, client):
        payload = {{**{obj}_payload, "date_of_birth": "no-es-una-fecha"}}
        response = client.post("/api/v1/{plural}/", json=payload)
        assert response.status_code == 422

    # prueba el endpoint de post con name vacio, lanza error
    def test_create_{obj}_empty_title(self, {obj}_payload, client):
        payload = {{**{obj}_payload, "username": ""}}
        response = client.post("/api/v1/{plural}/", json=payload)
        assert response.status_code == 422

    # prueba el endpoint de post si devuelve created_at y updated_at
    def test_create_{obj}_returns_timestamps(self, client):
        payload = {{
            "name": "name"
        }}
        response = client.post("/api/v1/{plural}/", json=payload)
        data = response.json()
        assert "created_at" in data
        assert "updated_at" in data


class TestGetAll{plural_title}:
    # prueba el endpoint de getall si devuelve lo que tiene hasta ahora
    def test_get_all_returns_list(self, client):
        response = client.get("/api/v1/{plural}/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "{plural}" in data
        assert isinstance(data["{plural}"], list)

    # prueba el endpoint de getall si contiene lo que fue creado por created_{obj}
    def test_get_all_contains_created_{obj}(self, created_{obj}, client):
        response = client.get("/api/v1/{plural}/")
        {plural} = response.json()["{plural}"]
        ids = [p["id"] for p in {plural}]
        assert created_{obj}["id"] in ids

    # prueba el endpoint de getall si devuelve todos los campos correspondientes del dto
    def test_get_all_{obj}_fields(self, created_{obj}, client):
        response = client.get("/api/v1/{plural}/")
        {plural} = response.json()["{plural}"]
        print(response.json())
        {obj} = next((p for p in {plural} if p["id"] == created_{obj}["id"]), None)
        assert {obj} is not None
        for field in ("name"):
            assert field in {obj}


class TestGet{pascal}ById:
    # prueba el endpoint de get si devuelve lo que fue creado por created_{obj} con su respectivo id
    def test_get_{obj}_by_id_success(self, created_{obj}, client):
        {obj}_id = created_{obj}["id"]
        response = client.get(f"/api/v1/{plural}/{{{obj}_id}}")
        assert response.status_code == 200
        assert response.json()["id"] == {obj}_id

    # prueba el endpoint de get si falla al consultar un id que no existe
    def test_get_{obj}_by_id_not_found(self, client):
        response = client.get("/api/v1/{plural}/id-que-no-existe-99999")
        assert response.status_code == 404

    # prueba el endpoint de get si contiene ciertos campos que fueron creados por created_{obj}
    def test_get_{obj}_by_id_returns_correct_data(self, created_{obj}, client):
        response = client.get(f"/api/v1/{plural}/{{created_{obj}['id']}}")
        data = response.json()
        assert data["name"] == created_{obj}["name"]


class TestUpdate{pascal}:
# prueba el endpoint de patch para actualizar N atributos
    def test_update_{obj}_by_id_success(self, created_{obj}, client):
        {obj}_id = created_{obj}["id"]
        update_payload = {{
            "status": "INACTIVE", 
            "bio": "biografia actualizada"
        }}
        response = client.patch(f"/api/v1/{plural}/{{{obj}_id}}", json=update_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "INACTIVE"
        assert data["bio"] == "biografia actualizada"

    # prueba el endpoint de patch para actualizar un {obj} con id inexistente, lanza error
    def test_update_{obj}_by_id_not_found(self, client):
        response = client.patch("/api/v1/{plural}/id-8382heds", json={{"status": "INACTIVE"}})
        assert response.status_code == 404

    # prueba el endpoint de patch para actualizar el status BANNED a SUSPENDED, lanza error
    def test_update_{obj}_discontinued_to_inactive_raises_error(self, created_{obj}, client):
        {obj}_id = created_{obj}["id"]
        # primero pasar a BANNED
        client.patch(f"/api/v1/{plural}/{{{obj}_id}}", json={{"status": "BANNED"}})
        # luego intentar pasar a SUSPENDED
        response = client.patch(f"/api/v1/{plural}/{{{obj}_id}}", json={{"status": "SUSPENDED"}})
        assert response.status_code == 422

    # prueba el endpoint de patch para actualizar y ver si update_at es mayor
    def test_update_{obj}_updates_updated_at(self, created_{obj}, client):
        {obj}_id = created_{obj}["id"]
        original_updated_at = created_{obj}["updated_at"]
        client.patch(f"/api/v1/{plural}/{{{obj}_id}}", json={{"description": "Nueva descripcion"}})
        response = client.get(f"/api/v1/{plural}/{{{obj}_id}}")
        new_updated_at = response.json()["updated_at"]
        # updated_at debe haber cambiado (o ser igual si es muy rápido — depende)
        assert new_updated_at >= original_updated_at

    # prueba el endpoint de patch al actualizar a un status que no existe
    def test_update_{obj}_invalid_status(self, created_{obj}, client):
        response = client.patch(f"/api/v1/{plural}/{{created_{obj}['id']}}", json={{"status": "INVALID"}})
        assert response.status_code == 422


class TestDelete{pascal}:
    # prueba el endpoint de delete 
    def test_delete_{obj}_by_id_success(self, {obj}_payload, client):
        # crear {obj} exclusivo para este test
        create_resp = client.post("/api/v1/{plural}/", json={obj}_payload)
        {obj}_id = create_resp.json()["id"]

        # eliminarlo segun el id
        delete_resp = client.delete(f"/api/v1/{plural}/{{{obj}_id}}")
        assert delete_resp.status_code == 204

        # verificar que ya no existe
        get_resp = client.get(f"/api/v1/{plural}/{{{obj}_id}}")
        assert get_resp.status_code == 404

    # prueba el endpoint de delete con un id inexistente
    def test_delete_{obj}_by_id_not_found(self, client):
        response = client.delete("/api/v1/{plural}/id-inexistente-jeje")
        assert response.status_code == 404

    # prueba el endpoint de delete 2 veces para ver si se elimino a la primera, si sale a la segunda tambien esta mal
    def test_delete_{obj}_by_id_idempotent(self, {obj}_payload, client):
        create_resp = client.post("/api/v1/{plural}/", json={obj}_payload)
        {obj}_id = create_resp.json()["id"]
        client.delete(f"/api/v1/{plural}/{{{obj}_id}}")
        second_delete = client.delete(f"/api/v1/{plural}/{{{obj}_id}}")
        assert second_delete.status_code == 404
'''


# ──────────────────────────────────────────────
# Construcción del árbol de archivos
# ──────────────────────────────────────────────

def build_file_tree(obj: str, pascal: str, base: Path) -> dict[Path, str]:
    """
    Retorna un diccionario {ruta: contenido} con todos los archivos a crear.
    Los __init__.py vacíos se representan con cadena vacía.
    """
    s = base / obj
    files: dict[Path, str] = {}

    # ── raíz del objeto
    files[s / "__init__.py"] = ""

    # ── domain
    files[s / "domain" / "__init__.py"] = ""
    files[s / "domain" / f"{obj}.py"] = tpl_domain_entity(obj, pascal)
    files[s / "domain" / f"{obj}_repository.py"] = tpl_domain_repository(obj, pascal)

    # ── application
    files[s / "application" / "__init__.py"] = ""
    files[s / "application" / "ports" / "__init__.py"] = ""
    files[s / "application" / "ports" / f"{obj}_dtos.py"] = tpl_dtos(obj, pascal)
    files[s / "application" / "use_cases" / "__init__.py"] = ""
    files[s / "application" / "use_cases" / f"create_{obj}.py"] = tpl_create_use_case(obj, pascal)
    files[s / "application" / "use_cases" / f"get_{obj}.py"] = tpl_get_use_case(obj, pascal)
    files[s / "application" / "use_cases" / f"update_{obj}.py"] = tpl_update_use_case(obj, pascal)
    files[s / "application" / "use_cases" / f"delete_{obj}.py"] = tpl_delete_use_case(obj, pascal)
    files[s / "application" / "services" / "__init__.py"] = ""
    files[s / "application" / "services" / f"{obj}_validator.py"] = tpl_validator(obj, pascal)

    # ── infrastructure / repositories
    files[s / "infrastructure" / "__init__.py"] = ""
    files[s / "infrastructure" / "repositories" / "__init__.py"] = ""
    files[s / "infrastructure" / "repositories" / f"{obj}_model.py"] = tpl_model(obj, pascal)
    files[s / "infrastructure" / "repositories" / f"{obj}_mapper.py"] = tpl_mapper(obj, pascal)
    files[s / "infrastructure" / "repositories" / f"sqlalchemy_{obj}_repository.py"] = tpl_sqlalchemy_repo(obj, pascal)

    # ── infrastructure / api
    files[s / "infrastructure" / "api" / "__init__.py"] = ""
    files[s / "infrastructure" / "api" / "v1" / "__init__.py"] = ""
    files[s / "infrastructure" / "api" / "v1" / "dependencies.py"] = tpl_dependencies(obj, pascal)
    files[s / "infrastructure" / "api" / "v1" / "endpoints" / "__init__.py"] = ""
    files[s / "infrastructure" / "api" / "v1" / "endpoints" / f"{obj}_router.py"] = tpl_router(obj, pascal)

    return files


def build_test_tree(obj: str, pascal: str, base: Path) -> dict[Path, str]:
    t = base / obj
    return {
        t / "__init__.py": "",
        t / f"test_{obj}_domain.py": tpl_test_domain(obj, pascal),
        t / f"test_{obj}_endpoints.py": tpl_test_endpoint(obj, pascal),
    }


# ──────────────────────────────────────────────
# Escritura y reporte
# ──────────────────────────────────────────────

RESET  = "\033[0m"
GREEN  = "\033[32m"
CYAN   = "\033[36m"
YELLOW = "\033[33m"
BOLD   = "\033[1m"

def write_files(files: dict[Path, str], dry_run: bool = False) -> list[Path]:
    created = []
    for path, content in files.items():
        if path.exists():
            print(f"  {YELLOW}~ skipped (ya existe){RESET}  {path}")
            continue
        if not dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        created.append(path)
        label = "(dry-run) " if dry_run else ""
        print(f"  {GREEN}+ {label}creado{RESET}  {path}")
    return created


def print_tree(obj: str, base_src: Path, base_tests: Path) -> None:
    print(f"\n{CYAN}{BOLD}Árbol generado:{RESET}")
    print(f"  {base_src}/{obj}/")
    lines = [
        "├── __init__.py",
        "├── domain/",
        f"│   ├── {obj}.py",
        f"│   └── {obj}_repository.py",
        "├── application/",
        "│   ├── ports/",
        f"│   │   └── {obj}_dtos.py",
        "│   └── use_cases/",
        f"│       ├── create_{obj}.py",
        f"│       ├── get_{obj}.py",
        f"│       ├── update_{obj}.py",
        f"│       └── delete_{obj}.py",
        "└── infrastructure/",
        "    ├── repositories/",
        f"    │   ├── {obj}_model.py",
        f"    │   ├── {obj}_mapper.py",
        f"    │   └── sqlalchemy_{obj}_repository.py",
        "    └── api/v1/",
        "        ├── dependencies.py",
        "        └── endpoints/",
        f"            └── {obj}_router.py",
    ]
    for line in lines:
        print(f"    {line}")
    print(f"\n  {base_tests}/{obj}/")
    print(f"    └── test_{obj}_domain.py")


# ──────────────────────────────────────────────
# Entrada principal
# ──────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera la estructura de un objeto de dominio en arquitectura hexagonal.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
ejemplos:
  python create_object.py
  python create_object.py --name tournament
  python create_object.py --name tournament_registration --base-path src
  python create_object.py --name match --dry-run
        """,
    )
    parser.add_argument("--name", help="Nombre del objeto en snake_case (ej: tournament)")
    parser.add_argument(
        "--base-path",
        default="src",
        help="Ruta base donde viven los objetos de dominio (default: src)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Muestra qué se crearía sin escribir ningún archivo",
    )
    return parser.parse_args()


def prompt_name() -> str:
    print(f"\n{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{BOLD} Generador de objetos de dominio — eSports Backend{RESET}")
    print(f"{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n")
    while True:
        raw = input("  Nombre del objeto (snake_case, ej: tournament): ").strip()
        if raw:
            return raw
        print("  El nombre no puede estar vacío. Intentá de nuevo.")


def main() -> None:
    args = parse_args()

    raw_name = args.name if args.name else prompt_name()

    try:
        obj = to_snake(raw_name)
    except ValueError as exc:
        print(f"\n  ERROR: {exc}")
        sys.exit(1)

    pascal = to_pascal(obj)
    base_src   = Path(args.base_path)
    base_tests = Path("tests")

    print(f"\n{BOLD}Objeto:{RESET}  {obj}  →  {CYAN}{pascal}{RESET}")
    print(f"{BOLD}Ruta:{RESET}    {base_src}/{obj}/")
    if args.dry_run:
        print(f"{YELLOW}{BOLD}[DRY-RUN]{RESET} No se escribirá ningún archivo.\n")
    else:
        print()

    # Verificar si ya existe
    target = base_src / obj
    if target.exists() and not args.dry_run:
        answer = input(
            f"  {YELLOW}La carpeta '{target}' ya existe. ¿Continuar de todas formas? [s/N]: {RESET}"
        ).strip().lower()
        if answer not in ("s", "si", "sí", "y", "yes"):
            print("  Cancelado.")
            sys.exit(0)

    # Generar y escribir archivos
    src_files   = build_file_tree(obj, pascal, base_src)
    test_files  = build_test_tree(obj, pascal, base_tests)
    all_files   = {**src_files, **test_files}

    write_files(all_files, dry_run=args.dry_run)

    # Árbol visual
    print_tree(obj, base_src, base_tests)

    # Recordatorios post-creación
    print(f"\n{YELLOW}{BOLD}Pasos manuales pendientes:{RESET}")
    print(tpl_alembic_hint(obj, pascal))
    print(tpl_main_hint(obj, pascal))

    total = len(all_files)
    print(f"{GREEN}{BOLD}✓ {total} archivos {'simulados' if args.dry_run else 'creados'} para '{obj}'.{RESET}\n")


if __name__ == "__main__":
    main()