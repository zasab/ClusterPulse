import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

config = context.config
# if config.config_file_name:
#     fileConfig(config.config_file_name)

from clustersense.db.models import Base  # noqa: E402
target_metadata = Base.metadata

def get_url() -> str:
    return os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://clustersense:clustersense@localhost:5432/clustersense",
    )

def run_migrations_offline() -> None:
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = create_engine(get_url(), poolclass=pool.NullPool, future=True)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()