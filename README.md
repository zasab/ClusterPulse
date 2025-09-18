# ClusterPulse
ClusterPulse — parse real(ish) HPC scheduler logs (Slurm-like), ingest to Postgres, serve metrics + ML predictions (job runtime, anomaly detection) via a Flask API and a tiny demo UI.

## Problem & users
HPC teams need visibility: which jobs/users/partitions are slow or failing, which queues are over-subscribed, and “how long will my job take?”
Users/beneficiaries: HPC admins (capacity planning, reliability), power users (job tuning), researchers (time estimates).
