# tests/test_repository.py
import pytest
from datetime import datetime, timezone
from sqlalchemy.exc import OperationalError

from clustersense.db.repository import insert_job_log, get_job_log_by_id, find_by_job_id
from clustersense.parsing.log_record import LogRecord

def test_insert_job_log_roundtrip():
    rec = LogRecord(
        ts=datetime(2025, 9, 1, 12, 34, 56, tzinfo=timezone.utc),
        cluster="clusterA",
        component="slurmctld",
        job_id=9001,  # use a unique job_id for this test
        user="zahra",
        account="projA",
        partition="cpu",
        nodes=2,
        ntasks=64,
        state="COMPLETED",
        exit_code="0:0",
        elapsed_seconds=12*60 + 34,
        cputime_seconds=26*60 + 48,
        req_mem_mb=4096,
        alloc_tres={"cpu": "64", "mem": 8192},
        raw="demo line",
    )
    try:
        new_id = insert_job_log(rec)
        job = get_job_log_by_id(new_id)
    except OperationalError:
        pytest.skip("Database not running")

    assert job is not None
    assert job.user == "zahra"
    assert job.job_id == 9001

def test_find_by_job_id_returns_inserted_records():
    # Arrange: insert two rows for a distinct job_id for THIS test
    jid = 9002
    rec1 = LogRecord(
        ts=datetime(2025, 9, 1, 12, 00, 00, tzinfo=timezone.utc),
        cluster="clusterA",
        component="slurmctld",
        job_id=jid,
        user="zahra",
        account="projA",
        partition="cpu",
        nodes=2,
        ntasks=64,
        state="RUNNING",
        exit_code=None,
        elapsed_seconds=60,
        cputime_seconds=120,
        req_mem_mb=2048,
        alloc_tres={"cpu": "64", "mem": 4096},
        raw="line1",
    )
    rec2 = LogRecord(
        ts=datetime(2025, 9, 1, 12, 5, 00, tzinfo=timezone.utc),
        cluster="clusterA",
        component="slurmctld",
        job_id=jid,
        user="zahra",
        account="projA",
        partition="cpu",
        nodes=2,
        ntasks=64,
        state="COMPLETED",
        exit_code="0:0",
        elapsed_seconds=300,
        cputime_seconds=600,
        req_mem_mb=2048,
        alloc_tres={"cpu": "64", "mem": 4096},
        raw="line2",
    )

    try:
        insert_job_log(rec1)
        insert_job_log(rec2)
        results = find_by_job_id(jid)
    except OperationalError:
        pytest.skip("Database not running")

    assert isinstance(results, list)
    assert len(results) >= 2
    # ordered by ts ascending
    assert results[0].ts <= results[1].ts
    assert all(r.job_id == jid for r in results)
    assert any(r.user == "zahra" for r in results)