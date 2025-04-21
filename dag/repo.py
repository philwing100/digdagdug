from dagster import repository
from .job import data_pipeline, example_job
from .sensors import new_user_sensor

@repository
def my_repo():
    return [
        data_pipeline,
        example_job,
        new_user_sensor
    ]
