import os
from sqlalchemy import create_engine

def get_engine():
    url = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://clustersense:clustersense@localhost:5432/clustersense"
    )
    return create_engine(url, echo=False, future=True)