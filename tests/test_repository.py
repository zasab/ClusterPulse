from clustersense.db.repository import *


def test_insert_job_log():
	record = LogRecord(
	    ts=datetime(2025, 9, 1, 12, 34, 56, tzinfo=timezone.utc),
	    cluster="clusterA",
	    component="slurmctld",
	    job_id=123,
	    user="zahra",
	    account="projA",
	    partition="cpu",
	    nodes=2,
	    ntasks=64,
	    state="COMPLETED",
	    exit_code="0:0",
	    elapsed_seconds=12*60 + 34,       # 754 seconds
	    cputime_seconds=(26*60 + 48),     # 1608 seconds
	    req_mem_mb=4096,                  # 4G = 4096 MB
	    alloc_tres={"cpu": "64", "mem": 8192},  # mem normalized to MB
	    raw="2025-09-01T12:34:56Z clusterA slurmctld[911]: ...",
	)

	new_id = insert_job_log(record)
	job = get_job_log_by_id(new_id)
	assert job is not None and job.user == "zahra"
