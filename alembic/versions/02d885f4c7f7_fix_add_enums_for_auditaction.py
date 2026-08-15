"""fix add enums for auditaction

Revision ID: 02d885f4c7f7
Revises: 199dfd43203a
Create Date: 2026-08-15 16:24:46.426267

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


revision: str = '02d885f4c7f7'
down_revision: Union[str, None] = '199dfd43203a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE auditaction ADD VALUE 'GETALL'")
    op.execute("ALTER TYPE auditaction ADD VALUE 'ALERT'")


def downgrade() -> None:
    pass
