from airflow.sdk import dag, task
from pendulum import datetime
from airflow.timetables.interval import CronDataIntervalTimetable


@dag(
    schedule=CronDataIntervalTimetable("@daily",timezone="Europe/Paris"),
    start_date=datetime(year=2026, month=1, day=26, tz="Europe/Paris"),
    end_date=datetime(year=2026, month=1, day=31, tz="Europe/Paris"),
    catchup=True
)
def incremental_load_dag():

    @task.python
    def incremental_data_fetch(**kwargs):
        # data_interval_start & data_interval_end are Airflow context variables
        # automatically injected into kwargs at runtime by the timetable/schedule.
        # They define the logical time window this DAG run is responsible for.
        date_interval_start = kwargs['data_interval_start']
        date_interval_end = kwargs['data_interval_end']
        print(f"Fetching data from {date_interval_start} to {date_interval_end}")

    @task.bash
    def incremental_data_process():
        return "echo 'Processing incremental data from {{ data_interval_start }} to {{ data_interval_end }}'"
    
    fetch_task = incremental_data_fetch()
    process_task = incremental_data_process()
    fetch_task >> process_task

# Instantiating the DAG
incremental_load_dag()