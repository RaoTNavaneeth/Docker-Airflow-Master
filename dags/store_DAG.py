from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.operators.email import EmailOperator

from pathlib import Path


from datacleaner import data_cleaner

default_args = {
    'owner': 'Airflow',
    # Reset to your appropriate date (Better to give 2-3 days previous)
    'start_date': datetime(2026, 1, 1), 
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

SQL_DIR = Path("/opt/airflow/sql")

CREATE_TABLE_SQL = (SQL_DIR / "create_table.sql").read_text()
INSERT_SQL = (SQL_DIR / "insert_into_table.sql").read_text()
SELECT_SQL = (SQL_DIR / "select_from_table.sql").read_text()

with DAG(
    dag_id="store_dag",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=True,
    template_searchpath=["/opt/airflow/sql"],
) as dag:

    t1=BashOperator(task_id='check_file_exists', bash_command='shasum /store_files/raw_store_transactions.csv', retries=2, retry_delay=timedelta(seconds=15))

    t2 = PythonOperator(task_id='clean_raw_csv', python_callable=data_cleaner)

    t3 = MySqlOperator(
    task_id="create_mysql_table",
    mysql_conn_id="mysql_conn",
    sql=CREATE_TABLE_SQL,
    )

    t4 = MySqlOperator(
    task_id="insert_into_table",
    mysql_conn_id="mysql_conn",
    sql=INSERT_SQL,
    )

    t5 = MySqlOperator(
    task_id="select_from_table",
    mysql_conn_id="mysql_conn",
    sql=SELECT_SQL,
    )
    t6 = BashOperator(
    task_id='move_file1',
    bash_command="""
    mv /store_files/location_wise_profit.csv \
       /store_files/location_wise_profit_{{ ds_nodash }}.csv
    """
    )
    t7 = BashOperator(
    task_id='move_file2',
    bash_command="""
    mv /store_files/store_wise_profit.csv \
       /store_files/store_wise_profit_{{ ds_nodash }}.csv
    """
    )
    t9 = EmailOperator(
    task_id='send_email',
    to='<<To Email ID>>',
    subject='Daily report generated',
    html_content="<h1>Congratulations! Your store reports are ready.</h1>",
    files=[
        '/store_files/location_wise_profit_{{ ds_nodash }}.csv',
        '/store_files/store_wise_profit_{{ ds_nodash }}.csv'
    ]
    )

    t8 = BashOperator(
    task_id='rename_raw',
    bash_command="""
    mv /store_files/raw_store_transactions.csv \
       /store_files/raw_store_transactions_{{ ds_nodash }}.csv
    """
)

    cleanup_reports = BashOperator(
    task_id='cleanup_old_reports',
    bash_command='rm -f /store_files/location_wise_profit.csv /store_files/store_wise_profit.csv'
    )
    t1 >> t2 >> t3 >> t4 >> cleanup_reports>> t5 >> [t6,t7] >> t8 >> t9

