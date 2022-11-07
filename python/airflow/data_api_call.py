"""
DAG file for auto labelling job.
"""

from datetime import timedelta, datetime

import os
from airflow.models import DAG
from airflow.operators.http_operator import SimpleHttpOperator
import logging
import json

DAG_NAME = "data_api_call"
TASK_DATA_API_CALL = "data_api_call"
CONNECTION_ID = "data_api_connection"

with DAG(DAG_NAME,
         description='collaboration with data api',
         schedule_interval=None,
         start_date=datetime(2018, 11, 1),
         catchup=False) as dag:
    def data_api_call(connection_id=CONNECTION_ID):
        return SimpleHttpOperator(
            task_id=TASK_DATA_API_CALL
            , http_conn_id=CONNECTION_ID
            , method="GET"
            , endpoint="/"
            # data="{\"id\":111333222}"
            , headers={"Content-Type": "application/json"}
            # response will be pushed to xcom with COLLABORATION_TASK_ID
            , xcom_push=True
            , log_response=True
            , extra_options={"verify": False, "cert": None}
        )

    data_api_call()

# Conn Id: data_api_connection
# Conn Type: HTTP
# Host: https://ipify.org
# Login(will be skipped): root
# Password(will be skipped): root