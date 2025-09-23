# src/clustersense/db/session.py

from sqlalchemy.orm import sessionmaker
from clustersense.db.config import get_engine

# Factory function that builds a new sessionmaker bound to our engine
def get_sessionmaker():
    engine = get_engine()
    return sessionmaker(bind=engine, future=True, expire_on_commit=False)