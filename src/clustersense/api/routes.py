# the route that calls my repository
# src/clustersense/api/routes.py

from flask import Blueprint, jsonify
from sqlalchemy.exc import OperationalError
from clustersense.db.repository import find_by_job_id
from clustersense.api.schemas import LogRecordOut
from dataclasses import asdict

api_bp = Blueprint("api", __name__)

@api_bp.get("/jobs/by-jobid/<job_id>")
def get_jobs_by_jobid(job_id: str):
    # Step 1: validate
    try:
        jid = int(job_id)
    except ValueError:
        return jsonify({"error": "job_id must be an integer"}), 400
    if jid < 0:
        return jsonify({"error": "job_id must be non-negative"}), 400

    # Step 2: query database
    try:
        records = find_by_job_id(jid)
    except OperationalError:
        return jsonify({"error": "database unavailable"}), 503

    # Step 3: convert to JSON
    payload = [LogRecordOut(**asdict(r)).model_dump(mode="json") for r in records]
    return jsonify(payload), 200