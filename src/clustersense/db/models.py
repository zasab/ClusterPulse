from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, BigInteger, Text, TIMESTAMP
# String for short, structured text with a max length.
# Text for large, unbounded text (like your raw log line).
from sqlalchemy.dialects.postgresql import JSONB
import sqlalchemy as sa


# all other classes inherit from it, all tables share the same metadata
# Consistency → you can later add mixins (e.g., created_at, updated_at)
# to Base and all models will get them.
class Base(DeclarativeBase):
    pass


class JobLog(Base):
	__tablename__ = 'job_logs'

	id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
	ts: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), nullable = False)
	cluster: Mapped[str] = mapped_column(Text, nullable=False)
	component: Mapped[str] = mapped_column(Text, nullable=False)

	job_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
	username: Mapped[str | None] = mapped_column(Text, nullable=True)
	account: Mapped[str | None] = mapped_column(Text, nullable=True)
	partition: Mapped[str | None] = mapped_column(Text, nullable=True)
	nodes: Mapped[int | None] = mapped_column(Integer, nullable=True)
	ntasks: Mapped[int | None] = mapped_column(Integer, nullable=True)
	state: Mapped[str | None] = mapped_column(Text, nullable=True)
	exit_code: Mapped[str | None] = mapped_column(Text, nullable=True)
	elapsed_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
	cputime_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
	req_mem_mb: Mapped[int | None] = mapped_column(Integer, nullable=True)
	alloc_tres: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

	raw: Mapped[str] = mapped_column(Text, nullable=False)

	__table_args__ = (
        sa.Index("ix_job_logs_job_id", "job_id")
    )



