class DomainException(Exception):
    """Excepción base del dominio."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class EntityNotFoundException(DomainException):
    """Se lanza cuando no se encuentra una entidad."""
    def __init__(self, entity: str, identifier: str):
        super().__init__(f"{entity} con id '{identifier}' no encontrado.")


class EntityAlreadyExistsException(DomainException):
    """Se lanza cuando la entidad ya existe."""
    def __init__(self, entity: str, field: str, value: str):
        super().__init__(f"{entity} con {field} '{value}' ya existe.")


class InvalidValueException(DomainException):
    """Se lanza cuando un valor de dominio es inválido."""
    pass
