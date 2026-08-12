from fastapi import Request
from fastapi.responses import JSONResponse

from src.shared.exceptions.domain_exceptions import (
    EntityNotFoundException,
    EntityAlreadyExistsException,
    InvalidValueException,
    DomainException,
)


async def entity_not_found_handler(request: Request, exc: EntityNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message},
    )


async def entity_already_exists_handler(request: Request, exc: EntityAlreadyExistsException):
    return JSONResponse(
        status_code=409,
        content={"detail": exc.message},
    )


async def invalid_value_handler(request: Request, exc: InvalidValueException):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.message},
    )


async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message},
    )
