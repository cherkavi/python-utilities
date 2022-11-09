# airflow

## bash_templating

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/bash_templating.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/bash_templating.py -->
```py
"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2015, 6, 1),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG("tutorial", default_args=default_args, schedule_interval=timedelta(1))

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = BashOperator(task_id="print_date", bash_command="date", dag=dag)

t2 = BashOperator(task_id="sleep", bash_command="sleep 5", retries=3, dag=dag)

templated_command = """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "{{ params.my_param }}"
    {% endfor %}
"""

t3 = BashOperator(
    task_id="templated",
    bash_command=templated_command,
    params={"my_param": "Parameter I passed in"},
    dag=dag,
)

t2.set_upstream(t1)
t3.set_upstream(t1)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## branch_dag

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/branch_dag.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/branch_dag.py -->
```py
from datetime import datetime, timedelta

from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.bash_operator import BashOperator

default_args = {
	'owner': 'airflow',
	'depend_on_past': False,
	'start_date': datetime(2018, 11, 5, 10, 00, 00),
	'retries': 1,
	'retry_delay': timedelta(minutes=1)
}

def get_activated_sources():
	request = "SELECT * FROM course.source"
	pg_hook = PostgresHook(postgre_conn_id="postgre_sql", schema="airflow_mdb")
	connection = pg_hook.get_conn()
	cursor = connection.cursor()
	cursor.execute(request)
	sources = cursor.fetchall()
	for source in sources:
		if source[1]:
			return source[0]
	return None

def source_to_use(**kwargs):
	ti = kwargs['ti']
	source = ti.xcom_pull(task_ids='hook_task')
	print("source fetch from XCOM: {}".format(source))
	return source

def check_for_activated_source(**kwargs):
	ti = kwargs['ti']
	return ti.xcom_pull(task_ids='xcom_task').lower()

with DAG('branch_dag',
	default_args=default_args,
	schedule_interval='@once') as dag:

	start_task 	= DummyOperator(task_id='start_task')
	hook_task 	= PythonOperator(task_id='hook_task', python_callable=get_activated_sources)
	xcom_task 	= PythonOperator(task_id='xcom_task', python_callable=source_to_use, provide_context=True)
	branch_task 	= BranchPythonOperator(task_id='branch_task', python_callable=check_for_activated_source, provide_context=True)
	mysql_task 	= BashOperator(task_id='mysql', bash_command='echo "MYSQL is activated"')
	postgresql_task = BashOperator(task_id='postgresql', bash_command='echo "PostgreSQL is activated"')
	s3_task 	= BashOperator(task_id='s3', bash_command='echo "S3 is activated"')
	mongo_task 	= BashOperator(task_id='mongo', bash_command='echo "Mongo is activated"')
	
	start_task >> hook_task >> xcom_task >> branch_task
	branch_task >> mysql_task
	branch_task >> postgresql_task
	branch_task >> s3_task
	branch_task >> mongo_task
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## cleaning_tweet

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/cleaning_tweet.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/cleaning_tweet.py -->
```py
import pandas as pd
import numpy as np
import re
from datetime import datetime as dt
from datetime import date, timedelta

# This script cleans the fetched tweets from the previous task "fetching_tweets"

LOCAL_DIR='/tmp/'

def main():
	# Read the csv produced by the "fetching_tweets" task
	tweets = pd.read_csv(LOCAL_DIR + 'data_fetched.csv')
	
	# Rename the columns of the dataframe
	tweets.rename(columns={'Tweet': 'tweet', 'Time':'dt', 'Retweet from': 'retweet_from', 'User':'tweet_user'}, inplace=True)
	
	# Drop the useless column "User" since all the tweets are written by Elon Musk
	tweets.drop(['tweet_user'], axis=1, inplace=True)
	
	# Add a column before_clean_len to know the size of the tweets before cleaning
	tweets['before_clean_len'] = [len(t) for t in tweets.tweet]
	
	# Remove @mention in tweets
	tweets['tweet'] = tweets['tweet'].apply(lambda tweet: re.sub(r'@[A-Za-z0-9]+', '', tweet))
	
	# Remove URL in tweets
	tweets['tweet'] = tweets['tweet'].apply(lambda tweet: re.sub('https?://[A-Za-z0-9./]+', '', tweet))
	
	# Remove all non letter charaters including numbers from the tweets
	tweets['tweet'] = tweets['tweet'].apply(lambda tweet: re.sub('[^a-zA-Z]', ' ', tweet))
	
	# Lower case all the tweets
	tweets['tweet'] = tweets['tweet'].str.lower()
	
	# Add after clean len column
	tweets['after_clean_len'] = [len(t) for t in tweets.tweet]
	
	# Changing date format
	yesterday = date.today() - timedelta(days=1)
	dt = yesterday.strftime("%Y-%m-%d")
	tweets['dt'] = dt	

	# Export cleaned dataframe
	tweets.to_csv(LOCAL_DIR + 'data_cleaned.csv', index=False)

if __name__ == '__main__':

	main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## data_api_call

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/data_api_call.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/data_api_call.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## docker_celery_dag

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/docker_celery_dag.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/docker_celery_dag.py -->
```py
import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.postgres_operator import PostgresOperator

default_args = {
	'owner': 'airflow',
	'start_date': dt.datetime(2018, 10, 25, 11, 30, 00),
	'retries': 0
}

with DAG('docker_celery_dag',
	default_args=default_args,
	schedule_interval='*/5 * * * *',
	catchup=False) as dag:

	opr_create_schema = PostgresOperator(task_id="create_schema_task", sql="CREATE SCHEMA IF NOT EXISTS docker_celery;", autocommit=True, database='airflow')
	opr_create_table = PostgresOperator(task_id="create_table_task", sql="CREATE TABLE IF NOT EXISTS docker_celery.task(id VARCHAR(50) PRIMARY KEY, timestamp TIMESTAMP);", autocommit=True, database='airflow')	

	opr_end = BashOperator(task_id='opr_end', bash_command='echo "Done"')

	opr_create_schema >> opr_create_table

	# Dynamic Definition of your DAG!!
	for counter in range(1, 4):
		task_id='opr_insert_' + str(counter)
		task_date=dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		opr_insert = PostgresOperator(task_id=task_id, 
						sql="INSERT INTO docker_celery.task (id, timestamp) VALUES ('" + task_id + "_" + task_date  + "', '" + task_date + "');",
						autocommit=True,
						database='airflow')
		opr_create_table >> opr_insert >> opr_end
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## dynamic_dag

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/dynamic_dag.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/dynamic_dag.py -->
```py
import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.postgres_operator import PostgresOperator

default_args = {
	'owner': 'airflow',
	'start_date': dt.datetime(2018, 10, 25, 11, 30, 00),
	'retries': 0
}

with DAG('dynamic_dag',
	default_args=default_args,
	schedule_interval='*/5 * * * *',
	catchup=False) as dag:
	
	opr_end = BashOperator(task_id='opr_end', bash_command='echo "Done"')

	# Dynamic Definition of your DAG!!
	for counter in range(1, 4):
		task_id='opr_insert_' + str(counter)
		task_date=dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		opr_insert = PostgresOperator(task_id=task_id, 
						sql="INSERT INTO local_executor.task (id, timestamp) VALUES ('" + task_id + "_" + task_date  + "', '" + task_date + "');",
						postgres_conn_id='postgre_sql',
						autocommit=True,
						database='airflow_mdb')
		opr_insert >> opr_end
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## hello_world

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/hello_world.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/hello_world.py -->
```py
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

from time import sleep
from datetime import datetime

def print_hello():
	sleep(5)
	return 'Hello World'

with DAG('hello_world_dag', description='First DAG', schedule_interval='*/10 * * * *', start_date=datetime(2018, 11, 1), catchup=False) as dag:
	dummy_task 	= DummyOperator(task_id='dummy_task', retries=3)
	python_task	= PythonOperator(task_id='python_task', python_callable=print_hello)

	dummy_task >> python_task
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## hook_dag

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/hook_dag.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/hook_dag.py -->
```py
from datetime import datetime, timedelta

from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
	'owner': 'airflow',
	'depend_on_past': False,
	'start_date': datetime(2018, 11, 5, 10, 00, 00),
	'retries': 1,
	'retry_delay': timedelta(minutes=1)
}

def get_activated_sources():
	request = "SELECT * FROM course.source"
	pg_hook = PostgresHook(postgres_conn_id="postgre_sql", schema="airflow_mdb") # This connection must be set from the Connection view in Airflow UI
	connection = pg_hook.get_conn() # Gets the connection from PostgreHook
	cursor = connection.cursor() # Gets a cursor to the postgreSQL database. Look at https://www.postgresql.org/docs/9.2/plpgsql-cursors.html for more information
	cursor.execute(request) # Executes the request
	sources = cursor.fetchall() # Fetchs all the data from the executed request
	for source in sources: # Does a simple print of each source to show that the hook works well. More on the next lesson
		print("Source: {0} - activated: {1}".format(source[0], source[1]))
	return sources

with DAG('hook_dag',
	default_args=default_args,
	schedule_interval='@once',
	catchup=False) as dag:

	start_task = DummyOperator(task_id='start_task')
	hook_task = PythonOperator(task_id='hook_task', python_callable=get_activated_sources)
	start_task >> hook_task
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## http_call

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/http_call.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/http_call.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## plugin_hook_dag

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/plugin_hook_dag.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/plugin_hook_dag.py -->
```py
import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.elasticsearch_plugin import ElasticsearchHook

default_args = {
        'owner': 'airflow',
        'start_date': dt.datetime(2018, 11, 25, 11, 30, 00),
        'concurrency': 1,
        'retries': 0
}

def do_some_stuff():
	es_hook = ElasticsearchHook()
	print(es_hook.info())

with DAG('plugin_hook_dag',
        default_args=default_args,
        schedule_interval='@once',
	catchup=False
	) as dag:

	hook_es = PythonOperator(task_id='hook_es', python_callable=do_some_stuff)
	opr_end = BashOperator(task_id='opr_end', bash_command='echo "Done"')
	hook_es >> opr_end
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## plugin_operator_dag

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/plugin_operator_dag.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/plugin_operator_dag.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## plugins

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/plugins/elasticsearch_plugin/__init__.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/plugins/elasticsearch_plugin/__init__.py -->
```py
from airflow.plugins_manager import AirflowPlugin

from elasticsearch_plugin.hooks.elasticsearch_hook import ElasticsearchHook

# Views / Blueprints / MenuLinks are instantied objects
class ElasticsearchPlugin(AirflowPlugin):
	name 			= "elasticsearch_plugin"
	operators 		= []
	sensors			= []
	hooks			= [ ElasticsearchHook ]
	executors		= []
	admin_views		= []
	flask_blueprints	= []
	menu_links		= []
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## plugins

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/plugins/elasticsearch_plugin/blueprints/__init__.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/plugins/elasticsearch_plugin/blueprints/__init__.py -->
```py
from elasticsearch_plugin.blueprints.elasticsearch_blueprint import ElasticsearchBlueprint

ELASTICSEARCH_PLUGIN_BLUEPRINTS = [
	ElasticsearchBlueprint
]
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## plugins

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/plugins/elasticsearch_plugin/blueprints/elasticsearch_blueprint.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/plugins/elasticsearch_plugin/blueprints/elasticsearch_blueprint.py -->
```py
from flask import Blueprint

# Creating a flask blueprint to integrate the templates and static folder
# This creates a blueprint named "elasticsearch_plugin" defined in the file __name__. The template folder is ../templates and static_folder is static
ElasticsearchBlueprint = Blueprint('elasticsearch', __name__, template_folder='../templates', static_folder='static', static_url_path='/static/')
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## plugins

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/plugins/elasticsearch_plugin/hooks/__init__.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/plugins/elasticsearch_plugin/hooks/__init__.py -->
```py

```
<!-- MARKDOWN-AUTO-DOCS:END -->



## plugins

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/plugins/elasticsearch_plugin/hooks/elasticsearch_hook.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/plugins/elasticsearch_plugin/hooks/elasticsearch_hook.py -->
```py
from airflow.hooks.base_hook import BaseHook
from airflow.utils.log.logging_mixin import LoggingMixin
from ssl import create_default_context

from elasticsearch import Elasticsearch

class ElasticsearchHook(BaseHook, LoggingMixin):
	"""
	Hook used to interact with Elasticsearch

	
	"""
	def __init__(self, elasticsearch_conn_id='elasticsearch_default'):
		conn = self.get_connection(elasticsearch_conn_id)
		
		conn_config = {}
		hosts = []

		if conn.host:
			hosts = conn.host.split(',')
		if conn.port:
			conn_config['port'] = int(conn.port)
		if conn.login:
			conn_config['http_auth'] = (conn.login, conn.password)

		conn_config['scheme'] = conn.extra_dejson.get('scheme', 'http')
		
		ssl_cert_path = conn.extra_dejson.get('cert_path', None)
		if ssl_cert_path:
			conn_config['ssl_context'] = create_default_context(cafile=ssl_cert_path)
		
		verify_certs = conn.extra_dejson.get('verify_certs', None)
		if verify_certs:
			conn_config['verify_certs'] = verify_certs

		conn_config['sniff_on_start'] = conn.extra_dejson.get('sniff_on_start', False)

		self.es 	= Elasticsearch(hosts, **conn_config)
		self.index 	= conn.schema

	def get_conn(self):
		return self.es

	def get_index(self):
		return self.index

	def set_index(self, index):
		self.index = index

	def search(self, index, body):
		self.set_index(index)
		res = self.es.search(index=self.index, body=body)
		return res

	def create_index(self, index, body):
		self.set_index(index)
		res = self.es.indices.create(index=self.index, body=body)
		return res

	def add_doc(self, index, doc_type, doc):
		self.set_index(index)
		res = self.es.index(index=index, doc_type=doc_type, body=doc)
		return res
	
	def info(self):
		return self.es.info()

	def ping(self):
		return self.es.ping()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## plugins

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/plugins/elasticsearch_plugin/menu_links/__init__.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/plugins/elasticsearch_plugin/menu_links/__init__.py -->
```py
from elasticsearch_plugin.menu_links.elasticsearch_link import ElasticsearchLink

ELASTICSEARCH_PLUGIN_LINKS = [
	ElasticsearchLink
]
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## plugins

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/plugins/elasticsearch_plugin/menu_links/elasticsearch_link.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/plugins/elasticsearch_plugin/menu_links/elasticsearch_link.py -->
```py
from flask_admin.base import MenuLink

ElasticsearchLink = MenuLink(category='Elasticsearch Plugin', name='More Info', url='https://unknown.com')
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## plugins

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/plugins/elasticsearch_plugin/operators/__init__.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/plugins/elasticsearch_plugin/operators/__init__.py -->
```py

```
<!-- MARKDOWN-AUTO-DOCS:END -->



## plugins

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/plugins/elasticsearch_plugin/operators/elasticsearch_operator.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/plugins/elasticsearch_plugin/operators/elasticsearch_operator.py -->
```py
import json
from airflow.models import BaseOperator
from psycopg2.extras import RealDictCursor

from airflow.hooks.postgres_hook import PostgresHook
from airflow.utils.decorators import apply_defaults

from elasticsearch_plugin.hooks.elasticsearch_hook import ElasticsearchHook

class PostgresToElasticsearchTransfer(BaseOperator):
	"""
	Moves data from PostgreSQL to Elasticsearch.
	In order to avoid the airflow worker to load all the data retrived from the PostgreSQL query into memory,
	we use server side cursor and fetch the rows using batches.
	
	:param sql: SQL query to execute against PostgreSQL.
	:type sql: str

	:param index: Index where to save the data into Elasticsearch
	:type index: str

	:param postgres_conn_id: source PostgreSQL connection
	:type postgres_conn_id: str

	:param elasticsearch_conn_id: source Elasticsearch connection
	:type elasticsearch_conn_id: str
	"""
	
	@apply_defaults
	def __init__(self, sql, index, postgres_conn_id='postgres_default', elasticsearch_conn_id='elasticsearch_default', *args, **kwargs):
		super(PostgresToElasticsearchTransfer, self).__init__(*args, **kwargs)
		self.sql 			= sql
		self.index			= index
		self.postgres_conn_id 		= postgres_conn_id
		self.elasticsearch_conn_id 	= elasticsearch_conn_id

	def execute(self, context):
		postgres 	= PostgresHook(postgres_conn_id=self.postgres_conn_id).get_conn()
		es		= ElasticsearchHook(elasticsearch_conn_id=self.elasticsearch_conn_id)

		self.log.info("Extracting data from PostgreSQL: %s", self.sql)

		with postgres.cursor(name="serverCursor", cursor_factory=RealDictCursor) as postgres_cursor:
			postgres_cursor.itersize=2000
			postgres_cursor.execute(self.sql)
			for row in postgres_cursor:
				doc = json.dumps(row, indent=2)
				es.add_doc(index=self.index, doc_type='external', doc=doc)
		postgres.close()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## plugins

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/plugins/elasticsearch_plugin/views/__init__.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/plugins/elasticsearch_plugin/views/__init__.py -->
```py
from elasticsearch_plugin.views.elasticsearch_view import ElasticsearchView

# By leaving empty the parameter "category" you will get a direct to link to your view. (no drop down menu) 
ELASTICSEARCH_PLUGIN_VIEWS = [
	ElasticsearchView(category='Elasticsearch Plugin', name='Elasticsearch Dashboard')	
]
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## plugins

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/plugins/elasticsearch_plugin/views/elasticsearch_view.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/plugins/elasticsearch_plugin/views/elasticsearch_view.py -->
```py
from flask_admin import BaseView, expose
from elasticsearch_plugin.hooks.elasticsearch_hook import ElasticsearchHook

class ElasticsearchView(BaseView):
	@expose('/', methods=['GET', 'POST'])
	def index(self):
		try:
			es = ElasticsearchHook()
			data = es.info()
			isup = es.ping()
		except:
			data = {}
			isup = False
		return self.render("elasticsearch_plugin.html", data=data, isup=isup)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## simple_dag_backfill

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/simple_dag_backfill.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/simple_dag_backfill.py -->
```py
import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
	'owner': 'airflow',
	'start_date': dt.datetime(2018, 12, 15, 22, 00, 00),
	'concurrency': 1,
	'retries': 0
}

with DAG('simple_dag_backfill',
	default_args=default_args,
	schedule_interval='*/10 * * * *') as dag:
	task_hello = BashOperator(task_id='hello', bash_command='echo "hello!"')
	task_bye = BashOperator(task_id='bye', bash_command='echo "bye!"')
	task_hello >> task_bye
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## sla_dag

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/sla_dag.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/sla_dag.py -->
```py
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta, datetime

def log_sla_miss(dag, task_list, blocking_task_list, slas, blocking_tis):
    print("SLA was missed on DAG {0}s by task id {1}s with task list: {2} which are " \
	"blocking task id {3}s with task list: {4}".format(dag.dag_id, slas, task_list, blocking_tis, blocking_task_list))

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 2, 4, 23, 15, 0),
    'email': None,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

with DAG('sla_dag', default_args=default_args, sla_miss_callback=log_sla_miss, schedule_interval="*/1 * * * *", catchup=False) as dag:

	t0 = DummyOperator(task_id='t0')

	t1 = BashOperator(task_id='t1', bash_command='sleep 15', sla=timedelta(seconds=5), retries=0)

	t0 >> t1
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## subdag_dag

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/subdag_dag.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/subdag_dag.py -->
```py
from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.operators.subdag_operator import SubDagOperator
from airflow.operators.dummy_operator import DummyOperator
from subdag_factory import subdag_factory

PARENT_DAG_NAME='subdag_dag'
SUBDAG_DAG_NAME='subdag'

with DAG(
	dag_id=PARENT_DAG_NAME,
	schedule_interval='*/10 * * * *',
	start_date=datetime(2018, 11, 5, 10, 00, 00),
	catchup=False
) as dag:
	start_task = DummyOperator(task_id='start')	
	subdag_task = SubDagOperator(
			subdag=subdag_factory(PARENT_DAG_NAME, SUBDAG_DAG_NAME, dag.start_date, dag.schedule_interval),
			task_id=SUBDAG_DAG_NAME
		)
	end_task = DummyOperator(task_id='end')
	start_task >> subdag_task >> end_task
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## subdag_factory

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/subdag_factory.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/subdag_factory.py -->
```py
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator

def subdag_factory(parent_dag_name, child_dag_name, start_date, schedule_interval):
	subdag = DAG(
		dag_id='{0}.{1}'.format(parent_dag_name, child_dag_name),
		schedule_interval=schedule_interval,
		start_date=start_date,
		catchup=False)
	with subdag:
		dop_list = [DummyOperator(task_id='subdag_task_{0}'.format(i), dag=subdag) for i in range(5)]
		#for i, dop in enumerate(dop_list):
		#	if i > 0:
		#		dop_list[i - 1] >> dop
	return subdag
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## twitter_dag_final

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/twitter_dag_final.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/twitter_dag_final.py -->
```py
# load the dependencie

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.hive_operator import HiveOperator
from airflow.contrib.sensors.file_sensor import FileSensor
from datetime import date, timedelta
from datetime import datetime as dt

# import the script files which are going be execute as Tasks by the DAG

import fetching_tweet
import cleaning_tweet

# Local directory where the data file ise
LOCAL_DIR='/tmp/'

# HDFS directory where the data file will be uploaded
HDFS_DIR='/tmp/'

# each DAG must have a unique identifier
DAG_ID = 'twitter_dag_final'

# start_time is a datetime object to indicate
# at which time your DAG should start (can be either in the past or future)
DAG_START_DATE=airflow.utils.dates.days_ago(1)

# schedule interval is a timedelta object
# here our DAG will be run every day
DAG_SCHEDULE_INTERVAL="@daily"

# default_args are the default arguments applied to the DAG
# and all inherited tasks
DAG_DEFAULT_ARGS = {
	'owner': 'airflow',
	'depends_on_past': False,
	'start_date': DAG_START_DATE,
	'retries': 1,
	'retry_delay': timedelta(minutes=1)
}

yesterday = date.today() - timedelta(days=1)
dt = yesterday.strftime("%Y-%m-%d")

with DAG(
	DAG_ID,
	default_args=DAG_DEFAULT_ARGS,
	schedule_interval=DAG_SCHEDULE_INTERVAL
	) as dag:
	
	# Initialise a FileSensor to watch if a new file is coming.
	# task_id must be unique
	# poke_interval give the time in seconds that the job should wait between each tries
	waiting_file_task = FileSensor(task_id='waiting_file_task', fs_conn_id='fs_default', filepath='/home/airflow/airflow_files/data.csv', poke_interval=15, dag=dag)

	# Initialise a PythonOperator to execute the fetching_tweet.py script
	fetching_tweet_task = PythonOperator(task_id='fetching_tweet_task', python_callable=fetching_tweet.main, dag=dag)

	# Initialise another PythonOperator to execute the cleaning_tweet.py script
	cleaning_tweet_task = PythonOperator(task_id='cleaning_tweet_task', python_callable=cleaning_tweet.main, dag=dag)

	# Initialise a BashOperator to upload the file into HDFS
	filename='data_cleaned.csv'
	load_into_hdfs_task = BashOperator(task_id='load_into_hdfs_task', bash_command='hadoop fs -put -f ' + LOCAL_DIR + filename + ' ' + HDFS_DIR, dag=dag)
	
	# Initialise a HiveOperator to transfer data from HDFS to HIVE table
	load_into_hive_task = HiveOperator(task_id='transfer_into_hive_task', hql="LOAD DATA INPATH '" + HDFS_DIR + filename + "' INTO TABLE tweets PARTITION(dt='" + dt + "')", dag=dag)

	waiting_file_task >> fetching_tweet_task >> cleaning_tweet_task >> load_into_hdfs_task >> load_into_hive_task
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## twitter_dag_v_1

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/twitter_dag_v_1.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/twitter_dag_v_1.py -->
```py
# load the dependencies
from airflow import DAG
from datetime import date, timedelta, datetime

# default_args are the default arguments applied to the DAG and all inherited tasks
DAG_DEFAULT_ARGS = {
	'owner': 'airflow',
	'depends_on_past': False,
	'retries': 1,
	'retry_delay': timedelta(minutes=1)
}

with DAG('twitter_dag_v1', start_date=datetime(2018, 10, 1), schedule_interval="@daily", default_args=DAG_DEFAULT_ARGS, catchup=False) as dag:
	None
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## twitter_dag_v_2

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/twitter_dag_v_2.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/twitter_dag_v_2.py -->
```py
# load the dependencies
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.hive_operator import HiveOperator
from airflow.contrib.sensors.file_sensor import FileSensor
from datetime import date, timedelta, datetime

import fetching_tweet
import cleaning_tweet

# default_args are the default arguments applied to the Dag's tasks
DAG_DEFAULT_ARGS = {
	'owner': 'airflow',
	'depends_on_past': False,
	'retries': 1,
	'retry_delay': timedelta(minutes=1)
}

with DAG('twitter_dag_v2', start_date=datetime(2018, 10, 1), schedule_interval="@daily", default_args=DAG_DEFAULT_ARGS, catchup=False) as dag:
	waiting_file_task = FileSensor(task_id="waiting_file_task", fs_conn_id="fs_default", filepath="/home/airflow/airflow_files/data.csv", poke_interval=5)

	fetching_tweet_task = PythonOperator(task_id="fetching_tweet_task", python_callable=fetching_tweet.main)

	cleaning_tweet_task = PythonOperator(task_id="cleaning_tweet_task", python_callable=cleaning_tweet.main)

	load_into_hdfs_task = BashOperator(task_id="load_into_hdfs_task", bash_command="hadoop fs -put -f /tmp/data_cleaned.csv /tmp/")

	transfer_into_hive_task = HiveOperator(task_id="transfer_into_hive_task", hql="LOAD DATA INPATH '/tmp/data_cleaned.csv' INTO TABLE tweets PARTITION(dt='2018-10-01')")

	waiting_file_task >> fetching_tweet_task >> cleaning_tweet_task >> load_into_hdfs_task >> transfer_into_hive_task
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## xcom_dag

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/airflow/xcom_dag.py) -->
<!-- The below code snippet is automatically added from ../../python/airflow/xcom_dag.py -->
```py
from datetime import datetime, timedelta

from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
	'owner': 'airflow',
	'depend_on_past': False,
	'start_date': datetime(2018, 11, 5, 10, 00, 00),
	'retries': 1,
	'retry_delay': timedelta(minutes=1)
}

# Read the table course.source to fetch the data and return the name of first source having its column "activated" sets to true
# No need to call xcom_push here since we use the keyword "return" which has the same effect.
def get_activated_sources():
	request = "SELECT * FROM course.source"
	pg_hook = PostgresHook(postgre_conn_id="postgre_sql", schema="airflow_mdb")
	connection = pg_hook.get_conn()
	cursor = connection.cursor()
	cursor.execute(request)
	sources = cursor.fetchall()
	for source in sources:
		if source[1]:
			return source[0]
	return None

def source_to_use(**kwargs):
	ti = kwargs['ti']
	source = ti.xcom_pull(task_ids='hook_task')
	print("source fetch from XCOM: {}".format(source))

with DAG('xcom_dag',
	default_args=default_args,
	schedule_interval='@once',
	catchup=False) as dag:

	start_task = DummyOperator(task_id='start_task')
	hook_task = PythonOperator(task_id='hook_task', python_callable=get_activated_sources)
	xcom_task = PythonOperator(task_id='xcom_task', python_callable=source_to_use, provide_context=True)
	start_task >> hook_task >> xcom_task
```
<!-- MARKDOWN-AUTO-DOCS:END -->


