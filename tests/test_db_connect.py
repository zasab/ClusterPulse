import pytest
from clustersense.db.config import get_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy import text


def test_db_connection():
    try:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
    except OperationalError:
        pytest.skip("Database is not running, skiping test. ")