# a Pydantic model to serialize LogRecord
# pydantic: It validates request/response data automatically
# By parsing incoming JSON into a BaseModel and checking it against type hints.

from datetime import datetime
from typing import Optional, Dict, Union
from pydantic import BaseModel

class LogRecordOut(BaseModel):
    ts: datetime
    cluster: str
    component: str
    job_id: Optional[int] = None
    user: Optional[str] = None
    account: Optional[str] = None
    partition: Optional[str] = None
    nodes: Optional[int] = None
    ntasks: Optional[int] = None
    state: Optional[str] = None
    exit_code: Optional[str] = None
    elapsed_seconds: Optional[int] = None
    cputime_seconds: Optional[int] = None
    req_mem_mb: Optional[int] = None
    alloc_tres: Optional[Dict[str, Union[int, str]]] = None
    raw: str