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

class Email:
    def __init__(self, value: str):
        value = value.strip()

        if len(value) < 5:
            raise InvalidValueException("El email debe tener al menos 5 caracteres.")
        if value.count("@") != 1:
            raise InvalidValueException("El email no tiene un formato válido.")

        self.value = value

    def __str__(self):
        return self.value

class Password:
    def __init__(self, value: str):
        if len(value) < 8:
            raise InvalidValueException("La contraseña debe tener al menos 8 caracteres.")
        if not any(c.isupper() for c in value):
            raise InvalidValueException(
                "La contraseña debe contener al menos una letra mayúscula."
            )
        if not any(c.islower() for c in value):
            raise InvalidValueException(
                "La contraseña debe contener al menos una letra minúscula."
            )
        if not any(c.isdigit() for c in value):
            raise InvalidValueException(
                "La contraseña debe contener al menos un número."
            )

        self.value = value

    def __str__(self):
        return self.valuefro

    