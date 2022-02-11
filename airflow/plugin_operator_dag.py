import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.elasticsearch_plugin import ElasticsearchHook
from airflow.operators.elasticsearch_plugin import PostgresToElasticsearchTransfer

default_args = {
        'owner': 'airflow',
        'start_date': dt.datetime(2018, 11, 25, 11, 30, 00),
        'concurrency': 1,
        'retries': 0
}

with DAG('plugin_operator_dag',
        default_args=default_args,
        schedule_interval='@once',
	catchup=False
	) as dag:
	
	opr_transfer = PostgresToElasticsearchTransfer(task_id='postgres_to_es', sql='SELECT * FROM course.source', index='sources')
	opr_end = BashOperator(task_id='opr_end', bash_command='echo "Done"')
	opr_transfer >> opr_end
