# src/clustersense/db/repository.py

from typing import Optional
from clustersense.db.session import get_sessionmaker
from clustersense.db.models import JobLog
from clustersense.parsing.log_record import LogRecord  # your dataclass
from datetime import datetime, timezone
from sqlalchemy import select


def insert_job_log(record: LogRecord) -> int:
    # Basic guard: ts/cluster/component are NOT NULL in DB
    if record.ts is None or not record.cluster or not record.component:
        raise ValueError("record.ts, record.cluster, and record.component are required")

    Session = get_sessionmaker()

    job = JobLog(
        ts=record.ts,
        cluster=record.cluster,
        component=record.component,
        job_id=record.job_id,
        username=record.user,
        account=record.account,
        partition=record.partition,
        nodes=record.nodes,
        ntasks=record.ntasks,
        state=record.state,
        exit_code=record.exit_code,
        elapsed_seconds=record.elapsed_seconds,
        cputime_seconds=record.cputime_seconds,
        req_mem_mb=record.req_mem_mb,
        alloc_tres=record.alloc_tres,
        raw=record.raw or ""
    )

    with Session() as s:
        s.add(job)
        s.commit()

        return int(job.id)


def get_job_log_by_id(job_id: int) -> Optional[LogRecord]:
    if job_id is None:
        raise ValueError("job_id is required")

    Session = get_sessionmaker()

    with Session() as s:
        row = s.get(JobLog, job_id)

        if row is None:
            return None

        return LogRecord(
            ts=row.ts,
            cluster=row.cluster,
            component=row.component,
            job_id=row.job_id,
            user=row.username,
            account=row.account,
            partition=row.partition,
            nodes=row.nodes,
            ntasks=row.ntasks,
            state=row.state,
            exit_code=row.exit_code,
            elapsed_seconds=row.elapsed_seconds,
            cputime_seconds=row.cputime_seconds,
            req_mem_mb=row.req_mem_mb,
            alloc_tres=row.alloc_tres,
            raw=row.raw,
        )


def find_by_job_id(job_id: int) -> list[LogRecord]:
    if job_id is None:
        raise ValueError("job_id is required")

    Session = get_sessionmaker()

    records =  []
    with Session() as s:
        rows = (
            s.query(JobLog)
            .filter(JobLog.job_id == job_id)
            .order_by(JobLog.ts.asc())
            .all())
        
        for row in rows:
            log_record = LogRecord(
                ts=row.ts,
                cluster=row.cluster,
                component=row.component,
                job_id=row.job_id,
                user=row.username,
                account=row.account,
                partition=row.partition,
                nodes=row.nodes,
                ntasks=row.ntasks,
                state=row.state,
                exit_code=row.exit_code,
                elapsed_seconds=row.elapsed_seconds,
                cputime_seconds=row.cputime_seconds,
                req_mem_mb=row.req_mem_mb,
                alloc_tres=row.alloc_tres,
                raw=row.raw,
            )

            records.append(log_record)

        return records


def find_by_username(
            username:str,
            ts_from: Optional[datetime] = None,
            ts_to: Optional[datetime] = None,
            limit: int | None = None,
            offset: int | None = None
        ) -> list[LogRecord]:
    
    if username is None or not username.strip():
        raise ValueError("username is required")
    username = username.strip()

    if (
        (ts_from is not None
            and ts_from.tzinfo is None)
        or (ts_to is not None
            and ts_to.tzinfo is None)
        ):
        raise ValueError("timestamps must be timezone-aware (e.g., UTC)")
    if ts_from is not None and ts_to is not None and ts_from >= ts_to:
        raise ValueError("ts_from must be < ts_to")

    if (
        limit is not None and 
        (limit < 1 or limit > 1000)
        ):
        raise ValueError("limit must be between 1 and 1000.")

    if offset is not None and offset < 0:
        raise ValueError("offset must be >=0")


    Session = get_sessionmaker()

    records = []

    with Session() as s:
        SQL_statement = (
            select(JobLog)
            .where(JobLog.username == username)
            .order_by(JobLog.ts.asc())
            )

        if ts_from is not None:
            SQL_statement = SQL_statement.where(JobLog.ts >= ts_from)

        if ts_to is not None:
            SQL_statement = SQL_statement.where(JobLog.ts < ts_to)

        if limit is not None:
            SQL_statement = SQL_statement.limit(limit)

        if offset is not None:
            SQL_statement = SQL_statement.offset(offset)


        rows = s.execute(SQL_statement).scalars().all()

        for row in rows:
            log_record = LogRecord(
                ts=row.ts,
                cluster=row.cluster,
                component=row.component,
                job_id=row.job_id,
                user=row.username,
                account=row.account,
                partition=row.partition,
                nodes=row.nodes,
                ntasks=row.ntasks,
                state=row.state,
                exit_code=row.exit_code,
                elapsed_seconds=row.elapsed_seconds,
                cputime_seconds=row.cputime_seconds,
                req_mem_mb=row.req_mem_mb,
                alloc_tres=row.alloc_tres,
                raw=row.raw,
            )

            records.append(log_record)

        print("records: ", records)
        return records


def find_by_state(state: str) -> list[LogRecord]: 
    if state is None:
        raise ValueError("state is required")
    
    Session = get_sessionmaker()

    records = []

    with Session() as s:
        rows = (
            s.query(JobLog)
            .filter(JobLog.state == state)
            .all()
        )

    for row in rows:
        log_record = LogRecord(
                ts=row.ts,
                cluster=row.cluster,
                component=row.component,
                job_id=row.job_id,
                user=row.username,
                account=row.account,
                partition=row.partition,
                nodes=row.nodes,
                ntasks=row.ntasks,
                state=row.state,
                exit_code=row.exit_code,
                elapsed_seconds=row.elapsed_seconds,
                cputime_seconds=row.cputime_seconds,
                req_mem_mb=row.req_mem_mb,
                alloc_tres=row.alloc_tres,
                raw=row.raw,
            )

        records.append(log_record)

    return records

def find_by_timerange(ts_from: datetime, ts_to: datetime) -> list[LogRecord]:
    if ts_from is None or ts_to is None:
        raise ValueError("ts_from and ts_to are required")
    if ts_from.tzinfo is None or ts_to.tzinfo is None:
        raise ValueError("timestamps must be timezone-aware (e.g., UTC)")
    if ts_from >= ts_to:
        raise ValueError("ts_from must be < ts_to")

    Session = get_sessionmaker()

    records = []

    with Session() as s:
        SQL_statement = (
            select(JobLog)
            .where(JobLog.ts >= ts_from, JobLog.ts < ts_to)
            .order_by(JobLog.ts.asc())
        )
        rows = s.execute(SQL_statement).scalars().all()


    for row in rows:
        log_record = LogRecord(
            ts=row.ts,
            cluster=row.cluster,
            component=row.component,
            job_id=row.job_id,
            user=row.username,
            account=row.account,
            partition=row.partition,
            nodes=row.nodes,
            ntasks=row.ntasks,
            state=row.state,
            exit_code=row.exit_code,
            elapsed_seconds=row.elapsed_seconds,
            cputime_seconds=row.cputime_seconds,
            req_mem_mb=row.req_mem_mb,
            alloc_tres=row.alloc_tres,
            raw=row.raw,
        )

        records.append(log_record)

    return records







