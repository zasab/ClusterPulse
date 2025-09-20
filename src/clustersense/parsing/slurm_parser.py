from clustersense.parsing.log_record import LogRecord
from typing import Optional, Dict, Union
from datetime import datetime
import re

def parse_ts(ts: str) -> Optional[datetime]:
    try:
        if ts.endswith('Z'):
            ts = ts[:-1] + '+00:00'
        
        return datetime.fromisoformat(ts)
    except ValueError:
        return None

def parse_job_id(jobid: str) -> Optional[int]:
    if jobid.isdigit():
        return int(jobid)
    else:
        return None

def parse_alloctres(alloctres: str) -> Optional[Dict[str, Union[int, str]]]:
    try:
        if not alloctres:
            return None
        items = [alloctre.split('=') for alloctre in alloctres.split(',')]
        items_dict = {}
        for [x, y] in items:
            if x == 'mem':
                mb = parse_mem(y)
                items_dict[x] = mb if mb is not None else y
            else:
                items_dict[x] = y

        return items_dict
    except Exception:
        return None

def parse_mem(reqmem:str) -> Optional[int]:
    reqmem_re = re.compile(r"^(?P<mem>\d+)(?P<unit>[A-Z]*)$")
    reqmem_match = reqmem_re.match(reqmem)
    if reqmem_match is None:
        return None
    mem = reqmem_match.group("mem")
    unit = reqmem_match.group("unit").upper()
    if unit in ["MB", "M"]:
        return int(mem)
    elif unit in ["GB", "G"]:
        return int(mem) * 1024
    elif unit in ["TB", "T"]:
        return int(mem) * 1024 * 1024
    else:
        return None

def hms_to_seconds(s: str) -> int | None:
    if not s or s.lower() == "unknown":
        return None
    try:
        if "-" in s:  # days included
            days, hms = s.split("-", 1)
            h, m, sec = map(int, hms.split(":"))
            return int(days)*86400 + h*3600 + m*60 + sec
        else:
            h, m, sec = map(int, s.split(":"))
            return h*3600 + m*60 + sec
    except Exception:
        return None


def parse_line(line:str) -> Optional[LogRecord]:
    head_re = re.compile(r'^(?P<ts>\S+)\s+(?P<cluster>\S+)\s+(?P<component>\S+):\s*(?P<rest>.*)$')
    m = head_re.match(line.strip())
    if not m:
        return None
    infos_parts = m
    ts = parse_ts(infos_parts.group('ts'))
    cluster = infos_parts.group('cluster')
    component = infos_parts.group('component')
    if '[' in component:
        component = component.split('[', 1)[0]
    rest = infos_parts.group('rest').split()
    infos_dict = {
        'ts': ts,
        'cluster': cluster,
        'component': component,
    }
    info_re = re.compile(r'(?P<key>\S+?)=(?P<value>.+)')
    for info in rest:
        info = info.strip()
        info_match = info_re.match(info)
        if info_match is None:
            continue

        key = info_match.group('key').lower()
        value = info_match.group('value')

        if key == 'jobid':
            infos_dict['job_id'] = parse_job_id(value)

        if key in ['user', 'account', 'state', 'partition']:
            infos_dict[key] = value

        if key == 'alloctres':
            infos_dict['alloc_tres'] = parse_alloctres(value)

        if key in ['ntasks', 'nodes']:
            if value.isdigit():
                infos_dict[key] = int(value)
            else:
                infos_dict[key] = None

        if key == 'reqmem':
            infos_dict['req_mem_mb'] = parse_mem(value)

        if key == 'elapsed':
            infos_dict['elapsed_seconds'] = hms_to_seconds(value)

        if key == 'cputime':
            infos_dict['cputime_seconds'] = hms_to_seconds(value)

        if key == 'exitcode':
            infos_dict['exit_code'] = value

    infos_dict['raw'] = line

    return LogRecord(**infos_dict)

data = '2025-09-01T12:34:56Z clusterA slurmctld[911]: JobId=123 User=zahra Account=projA Partition=cpu Nodes=2 NTasks=64 State=COMPLETED ExitCode=0:0 Elapsed=00:12:34 CPUTime=00:26:48 ReqMem=4G AllocTRES=cpu=64,mem=8G'
print(parse_line(data))