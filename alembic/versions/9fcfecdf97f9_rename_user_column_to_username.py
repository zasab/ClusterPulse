"""rename user column to username

Revision ID: 9fcfecdf97f9
Revises: 9668ec271f70
Create Date: 2025-09-23 13:53:26.062827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9fcfecdf97f9'
down_revision: Union[str, Sequence[str], None] = '9668ec271f70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("job_logs", "user", new_column_name="username")


def downgrade() -> None:
    op.alter_column("job_logs", "username", new_column_name="user")
