from src.user.domain.user import User
from src.user.infrastructure.repositories.user_model import UserModel


class UserMapper:
    """Convierte entre la entidad de dominio y el modelo de persistencia."""

    @staticmethod
    def to_domain(model: UserModel) -> User:
        return User(
            id=model.id,
            name=model.name,
            date_of_birth=model.date_of_birth,
            status=model.status,
            bio=model.bio,
            image_url=model.image_url,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(user: User) -> UserModel:
        return UserModel(
            id=user.id,
            name=user.name,
            date_of_birth=user.date_of_birth,
            status=user.status,
            bio=user.bio,
            image_url=user.image_url,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
