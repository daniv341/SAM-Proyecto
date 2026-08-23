import asyncio
from datetime import datetime, timezone
import getpass

from src.user.domain.user import User, Role
from src.user.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.shared.database.engine import AsyncSessionLocal
from src.shared.config.security import hash_password
from ulid import ULID

from src.log.domain.log import Log
from src.log.infrastructure.repositories.sqlalchemy_log_repository import SQLAlchemyLogRepository

async def create_admin():
    email = input("Admin email: ").strip()
    password = getpass.getpass("Admin password: ")
    password_confirmation = getpass.getpass("Confirm password: ")

    if password != password_confirmation:
        print("Las contraseñas no coinciden.")
        return

    async with AsyncSessionLocal() as session:
        repo = SQLAlchemyUserRepository(session)
        repo_log = SQLAlchemyLogRepository(session)

        existing_user = await repo.find_by_email(email)

        if existing_user:
            print(f"Ya existe un usuario con el email {email}.")
            return

        admin = User(
            id=str(ULID()),
            name="admin",
            email=email,
            password=hash_password(password),
            date_of_birth=datetime(2001, 1, 19, tzinfo=timezone.utc),
            role=Role.ADMIN,
        )

        await repo.save(admin)
        await session.commit()

        print(f"Admin creado correctamente: {email}")

        log = Log(
            id=str(ULID()),
            action="CREATE",
            entity_type="USER",
            entity_id=admin.id,
            description=f"User {admin.name} with Email {admin.email} created"
        )
        # llamas a save del repositorio de log
        await repo_log.save(log)

if __name__ == "__main__":
    asyncio.run(create_admin())