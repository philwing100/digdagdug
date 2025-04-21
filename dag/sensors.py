from dagster import sensor, RunRequest
import supabase  # use your Supabase client here
import datetime
from .job import example_job
from api import call_stored_proc_modular

latest_seen_id = None  # Simple global state to track last seen row

@sensor(job=example_job)
def new_user_sensor(context):
    global latest_seen_id

    try:
        latest = call_stored_proc_modular("get_latest")
        if not latest:
            context.log.info("No new rows found.")
            return None

        row = latest[0]  # Supabase returns list of dicts
        latest_id = row["id"]
        context.log.info("latest_id: ",latest_id)

        print(latest_id)

        return None
    except Exception as e:
        context.log.error(f"Sensor failed: {e}")
        return None
