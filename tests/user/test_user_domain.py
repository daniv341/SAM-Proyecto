import pytest
from datetime import datetime, timezone

from src.user.domain.user import User, UserStatus
from src.shared.exceptions.domain_exceptions import InvalidValueException
from src.user.domain.user_validate import Name

def make_user(**overrides) -> User:
    """Factory con valores válidos por defecto para tests."""
    defaults = dict(
        id="01JTEST00000000000000000001",
        name="Test User",
        date_of_birth=datetime(1990, 1, 1, tzinfo=timezone.utc),
        status=UserStatus.ACTIVE,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    defaults.update(overrides)
    return User(**defaults)


class TestCreateUser:
    def test_create_valid(self):
        user = make_user()
        assert user.name == "Test User"
        assert user.status == UserStatus.ACTIVE

class TestName:
    def test_invalid_username(self):
        with pytest.raises(InvalidValueException):
            Name("ab")

    def test_valid_username(self):
        name = Name("Toad18")
        assert name.value == "Toad18"

class TestStatus:
    def test_ban_user(self):
        status = UserStatus.BANNED
        assert status.value == UserStatus.BANNED

    def test_active_user(self):
        status = UserStatus.ACTIVE
        assert status.value == UserStatus.ACTIVE

    def test_cannot_suspend_banned_user(self):
        user = make_user(status=UserStatus.BANNED)
        with pytest.raises(InvalidValueException):
            user.banned_changed_to_suspended(UserStatus.SUSPENDED)
        assert user.status == UserStatus.BANNED

