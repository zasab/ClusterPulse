"""add index on job_id column

Revision ID: 854edec54aaf
Revises: 9fcfecdf97f9
Create Date: 2025-09-23 16:04:51.029265

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '854edec54aaf'
down_revision: Union[str, Sequence[str], None] = '9fcfecdf97f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "ix_job_logs_job_id",   # index name
        "job_logs",             # table name
        ["job_id"],             # column(s)
        unique=False
    )

def downgrade() -> None:
    op.drop_index("ix_job_logs_job_id", table_name="job_logs")
