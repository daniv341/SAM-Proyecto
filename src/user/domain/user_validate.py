from src.shared.exceptions.domain_exceptions import InvalidValueException

class Name:
    def __init__(self, value: str):
        value = value.strip()

        if len(value) < 3:
            raise InvalidValueException("El name debe tener al menos 3 caracteres.")
        if len(value) > 50:
            raise InvalidValueException("El name no puede superar 50 caracteres.")

        self.value = value

    def __str__(self):
        return self.value