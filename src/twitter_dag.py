from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from twitter_scraper import get_tweets_from_user, get_my_timeline


# DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 2, 10),
    "email": ["tzj.daryl@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": True,
    "retries": 1,
    "retry_delay": timedelta(minutes=15),
}

dag = DAG(
    "twitter_dag",
    default_args=default_args,
    description="Getting started with Airflow DAGS",
    schedule_interval="0 * * * *",
    catchup=False
)

# Task 1
first_task = PythonOperator(
    task_id="get_tweets_from_coindesk", python_callable=get_tweets_from_user, dag=dag
)

# Task 2
second_task = PythonOperator(
    task_id="get_my_timeline", python_callable=get_my_timeline, dag=dag
)

# Set task order
first_task >> second_task
