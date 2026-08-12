from src.shared.exceptions.domain_exceptions import InvalidValueException

class Description:
    def __init__(self, value: str):
        value = value.strip()

        if len(value) < 3:
            raise InvalidValueException("La description debe tener al menos 3 caracteres.")
        if len(value) > 100:
            raise InvalidValueException("La description no puede superar 100 caracteres.")

        self.value = value

    def __str__(self):
        return self.value