"""add role in user

Revision ID: 70cd2c3423d8
Revises: aacb59f1100c
Create Date: 2026-08-23 15:08:48.419086

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


revision: str = '70cd2c3423d8'
down_revision: Union[str, None] = 'aacb59f1100c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    role_enum = sa.Enum(
        'USER',
        'ADMIN',
        name='role'
    )

    role_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        'users',
        sa.Column(
            'role',
            role_enum,
            nullable=False,
            server_default='USER'
        )
    )

    op.alter_column('users', 'role', server_default=None)


def downgrade() -> None:
    op.drop_column('users', 'role')

    role_enum = sa.Enum(
        'USER',
        'ADMIN',
        name='role'
    )

    role_enum.drop(op.get_bind(), checkfirst=True)
