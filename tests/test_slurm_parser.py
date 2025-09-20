from clustersense.parsing.slurm_parser import parse_line
from clustersense.parsing.log_record import LogRecord
from datetime import timezone


def test_basic_line():
	line = "2025-09-01T12:34:56Z clusterA slurmctld[911]: JobId=123 User=zahra"
	record = parse_line(line)
	assert record is not None
	assert isinstance(record, LogRecord)
	assert record.ts.tzinfo == timezone.utc
	assert record.job_id == 123
	assert record.user == 'zahra'
	assert record.cluster == 'clusterA'
	assert record.component == 'slurmctld'
	assert record.raw.startswith('2025-09-01T12:34:56Z ')

def test_parse_mem():
	line = "2025-09-01T12:34:56Z cA slurmctld[11]: JobId=1 ReqMem=8G"
	record = parse_line(line)
	assert record.req_mem_mb == 8192

def test_hms_to_seconds():
	line = "2025-09-01T12:34:56Z cA slurmctld[11]: JobId=2 Elapsed=01:02:03 CPUTime=2-00:00:00"
	record = parse_line(line)
	assert record.elapsed_seconds == 3723
	assert record.cputime_seconds == 172800