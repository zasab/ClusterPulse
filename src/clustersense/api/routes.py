# the route that calls my repository

from flask import Blueprint, jsonify
from sqlalchemy.exc import OperationalError
from clustersense.db.repository import find_by_job_id
from clustersense.api.schemas import LogRecordOut

api_bp = Blueprint("api", __name__)

@api_bp.get("/jobs/by-jobid/<int:job_id>")
def get_jobs_by_jobid(job_id: int):
    if job_id < 0:
        return jsonify({"error": "job_id must be non-negative"}), 400

    try:
        records = find_by_job_id(job_id)
    except OperationalError:
        return jsonify({"error": "database unavailable"}), 503

    payload = [LogRecordOut(**r.__dict__).model_dump() for r in records]
    return jsonify(payload), 200