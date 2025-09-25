import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError
from clustersense.db.config import get_engine

def test_job_logs_indexes_exist():
    try:
        engine = get_engine()
        insp = inspect(engine)
        idx_names = {ix["name"] for ix in insp.get_indexes("job_logs")}
    except OperationalError:
        pytest.skip("Database not running")

    expected = {
        "ix_job_logs_job_id"
    }
    assert expected.issubset(idx_names)