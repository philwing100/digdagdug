from dagster import job, repository
from .ops import read_csv_op, clean_data_op, send_to_supabase_op

@job
def data_pipeline():
    send_to_supabase_op(clean_data_op(read_csv_op()))

@job
def example_job():
    print("Sensor fired")  # You can also make this a proper op if needed
