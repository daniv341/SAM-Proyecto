import pytest
from datetime import datetime, timezone

from src.vulnerabilitie.domain.vulnerabilitie import Vulnerabilitie, Severity
from src.shared.exceptions.domain_exceptions import InvalidValueException

from src.vulnerabilitie.domain.vulnerabilitie_validate import Description

def make_vulnerabilitie(**overrides) -> Vulnerabilitie:
    """Factory con valores válidos por defecto para tests."""
    defaults = dict(
        id="01JTEST00000000000000000001",
        cve="CVE-2026-121",
        description="hola que hace",
        severity=Severity.MEDIUM,
        url="jjjsjfjs",
        mitigation=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    defaults.update(overrides)
    return Vulnerabilitie(**defaults)


class TestCreateVulnerabilitie:
    def test_create_valid(self):
        vulnerabilitie = make_vulnerabilitie()
        assert vulnerabilitie.cve == "CVE-2026-121"

class TestName:
    def test_invalid_description(self):
        with pytest.raises(InvalidValueException):
            Description("a")

    def test_valid_description(self):
        description = Description("nombre")
        assert description.value == "nombre"
