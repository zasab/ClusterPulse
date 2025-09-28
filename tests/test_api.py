import pytest
from sqlalchemy.exc import OperationalError

from datetime import datetime, timezone
from clustersense.db.repository import insert_job_log
from clustersense.parsing.log_record import LogRecord

def _insert_two_rows(job_id: int):
    r1 = LogRecord(
        ts=datetime(2025,9,1,12,0,0,tzinfo=timezone.utc),
        cluster="clusterA", component="slurmctld",
        job_id=job_id, user="zahra", account="projA", partition="cpu",
        nodes=2, ntasks=64, state="RUNNING", exit_code=None,
        elapsed_seconds=60, cputime_seconds=120, req_mem_mb=2048,
        alloc_tres={"cpu":"64","mem":4096}, raw="line1"
    )
    r2 = LogRecord(
        ts=datetime(2025,9,1,12,5,0,tzinfo=timezone.utc),
        cluster="clusterA", component="slurmctld",
        job_id=job_id, user="zahra", account="projA", partition="cpu",
        nodes=2, ntasks=64, state="COMPLETED", exit_code="0:0",
        elapsed_seconds=300, cputime_seconds=600, req_mem_mb=2048,
        alloc_tres={"cpu":"64","mem":4096}, raw="line2"
    )
    insert_job_log(r1)
    insert_job_log(r2)

def _insert_two_rows_specific_username(username: str):
    r1 = LogRecord(
        ts=datetime(2025,9,1,12,0,0,tzinfo=timezone.utc),
        cluster="clusterA", component="slurmctld",
        job_id="42366728", user=username, account="projA", partition="cpu",
        nodes=2, ntasks=64, state="RUNNING", exit_code=None,
        elapsed_seconds=60, cputime_seconds=120, req_mem_mb=2048,
        alloc_tres={"cpu":"64","mem":4096}, raw="line1"
    )
    r2 = LogRecord(
        ts=datetime(2025,9,1,12,10,0,tzinfo=timezone.utc),
        cluster="clusterA", component="slurmctld",
        job_id="42366728", user=username, account="projA", partition="cpu",
        nodes=2, ntasks=64, state="COMPLETED", exit_code="0:0",
        elapsed_seconds=300, cputime_seconds=600, req_mem_mb=2048,
        alloc_tres={"cpu":"64","mem":4096}, raw="line2"
    )
    insert_job_log(r1)
    insert_job_log(r2)

def test_get_jobs_by_jobid_ok(client):
    job_id = 424242
    try:
        _insert_two_rows(job_id)
    except OperationalError:
        pytest.skip("Database not running")

    resp = client.get(f"/api/jobs/by-jobid/{job_id}")
    assert resp.status_code == 200

    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2
    assert {"ts","cluster","component","job_id","user","state","raw"}.issubset(data[0].keys())
    assert data[0]["ts"] <= data[1]["ts"]

def test_get_jobs_by_jobid_bad_input(client):
    resp = client.get("/api/jobs/by-jobid/-5")
    assert resp.status_code == 400

def test_get_job_by_id(client):
    resp = client.get("/api/jobs/by-jobid/123")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert any(job["user"] == "zahra" for job in data)

def test_get_jobs_by_username_ok(client):
    username = "Nabaut"
    try:
        _insert_two_rows_specific_username(username)
    except OperationalError:
        pytest.skip("Datanase not running")

    
    resp = client.get(f"/api/jobs/by-username/{username}")
    assert resp.status_code == 200

    data = resp.get_json(resp)
    assert isinstance(data, list)
    assert len(data) >= 2
    assert {"ts","cluster","component","job_id","user","state","raw"}.issubset(data[0].keys())

def test_get_jobs_by_username_bad_input(client):
    resp = client.get("/api/jobs/by-username/-544")
    assert resp.status_code == 400

def test_get_jobs_by_state_ok(client):
    state = 'RUNNING'
    try:
        resp = client.get(f"/api/jobs/by-state/{state}")
    except OperationalError:
        pytest.skip("Database not running")
    
    assert resp.status_code == 200
    data = resp.get_json(resp)
    assert isinstance(data, list)
    assert len(data) >= 2
    assert {"ts","cluster","component","job_id","user","state","raw"}.issubset(data[0].keys())

def test_get_jobs_by_state_bad_input(client):
    resp = client.get("/api/jobs/by-state/nnn")
    assert resp.status_code == 400






    