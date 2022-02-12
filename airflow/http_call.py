"""
DAG file for auto labelling job.
"""

from datetime import timedelta, datetime

import os

from airflow.decorators import task, dag
from airflow.models import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
import logging
import json


DAG_NAME = "data_api_call"
TASK_DATA_API_CALL = "data_api_call"
CONNECTION_ID="data_api_connection"


@dag(
    schedule_interval="0 0 * * *",
    start_date=datetime.today() - timedelta(days=2),
    dagrun_timeout=timedelta(minutes=60),
)
def collaboration_with_data_api():
    @task
    def read_from_rest():
        return SimpleHttpOperator(
                task_id=TASK_DATA_API_CALL,
                http_conn_id=CONNECTION_ID,
                method="GET",
                endpoint="/",
                # data="{\"id\":111333222}",
                headers={"Content-Type": "application/json"},
                # response will be pushed to xcom with COLLABORATION_TASK_ID
                xcom_push=True,
                log_response=True,
            )

    read_from_rest()

dag=collaboration_with_data_api()
