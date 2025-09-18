from log_record import LogRecord
from typing import Optional, Dict
from datetime import datetime

def parse_ts(ts: str) -> Optional[datetime]:
    try:
        date = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
        return date
    except ValueError:
        return None

def parse_job_id(jobid: str) -> Optional[int]:
    try:
        if jobid.isdigit():
            return int(jobid)
        else:
            return None
    except ValueError:
        return None

def parse_alloctres(alloctres: str) -> Optional[Dict[str, str]]:
    try:
        items = [alloctre.split('=') for alloctre in alloctres.split(',')]
        items_dict = {}
        for [x, y] in items:
            items_dict[x] = y

        return items_dict
    except Exception:
        return None

def parse_line(line:str) -> Optional[LogRecord]:
    infos = line.split()
    ts = parse_ts(infos[0].strip())
    infos_dict = {
        'ts': ts
    }
    for info in infos:
        info = info.strip()
        if '=' in info:
            [key, value] = info.split('=', maxsplit=1)
            key = key.strip().lower()
            value = value.strip()
            if key == 'jobid':
                infos_dict['job_id'] = parse_job_id(value)

            if key in ['user', 'account', 'state', 'cluster']:
                infos_dict[key] = value

            if key == 'alloctres':
                infos_dict['alloctres'] = parse_alloctres(value)

    print(infos_dict)

data = '2025-09-01T12:34:56Z clusterA slurmctld[911]: JobId=123 User=zahra Account=projA Partition=cpu Nodes=2 NTasks=64 State=COMPLETED ExitCode=0:0 Elapsed=00:12:34 CPUTime=00:26:48 ReqMem=4G AllocTRES=cpu=64,mem=8G'
parse_line(data)