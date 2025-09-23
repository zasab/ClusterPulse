"""create job_logs table

Revision ID: 9668ec271f70
Revises: 
Create Date: 2025-09-23 09:30:59.677760

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9668ec271f70'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "job_logs",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("ts", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("cluster", sa.Text, nullable=False),
        sa.Column("component", sa.Text, nullable=False),
        sa.Column("job_id", sa.BigInteger, nullable=True),
        sa.Column("user", sa.Text, nullable=True),
        sa.Column("account", sa.Text, nullable=True),
        sa.Column("partition", sa.Text, nullable=True),
        sa.Column("nodes", sa.Integer, nullable=True),
        sa.Column("ntasks", sa.Integer, nullable=True),
        sa.Column("state", sa.Text, nullable=True),
        sa.Column("exit_code", sa.Text, nullable=True),
        sa.Column("elapsed_seconds", sa.Integer, nullable=True),
        sa.Column("cputime_seconds", sa.Integer, nullable=True),
        sa.Column("req_mem_mb", sa.Integer, nullable=True),
        sa.Column("alloc_tres", sa.dialects.postgresql.JSONB, nullable=True),
        sa.Column("raw", sa.Text, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("job_logs")
