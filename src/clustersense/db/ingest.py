
from pathlib import Path
from clustersense.parsing.slurm_parser import parse_line
from clustersense.db.repository import insert_job_log

def ingest_log_file(file_path: str) -> int:
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(p)
    inserted = 0
    with p.open(encoding="utf-8") as f:
        for line in f:
            rec = parse_line(line)
            if rec is None:
                continue
            insert_job_log(rec)
            inserted += 1
    return inserted


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python -m clustersense.db.ingest /path/to/fake_slurm.log")
    ingest_log_file(sys.argv[1])