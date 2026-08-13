from src.shared.exceptions.domain_exceptions import InvalidValueException

class CVE:
    def __init__(self, value: str):
        value = value.strip()

        if len(value) < 5:
            raise InvalidValueException("La CVE debe tener al menos 5 caracteres.")

        self.value = value

    def __str__(self):
        return self.value

class Description:
    def __init__(self, value: str):
        value = value.strip()

        if len(value) < 3:
            raise InvalidValueException("La description debe tener al menos 3 caracteres.")
        if len(value) > 200:
            raise InvalidValueException("La description no puede superar 200 caracteres.")

        self.value = value

    def __str__(self):
        return self.value