import pytest
from datetime import datetime, timezone

from src.workstation.domain.workstation import Workstation, WorkstationStatus, Type, Area
from src.shared.exceptions.domain_exceptions import InvalidValueException
from src.workstation.domain.workstation_validate import Description

def make_workstation(**overrides) -> Workstation:
    """Factory con valores válidos por defecto para tests."""
    defaults = dict(
        id="01JTEST00000000000000000001",
        user="fsksdkjsjjkjfk",
        status=WorkstationStatus.ACTIVE,
        type=Type.DESKTOP,
        area=Area.SUPPORT,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    defaults.update(overrides)
    return Workstation(**defaults)


class TestCreateWorkstation:
    def test_create_valid(self):
        workstation = make_workstation()
        assert workstation.user == "fsksdkjsjjkjfk"
        assert workstation.status == WorkstationStatus.ACTIVE

class TestDescription:
    def test_invalid_description(self):
        with pytest.raises(InvalidValueException):
            Description("a")

    def test_valid_description(self):
        description = Description("descripcion")
        assert description.value == "descripcion"
