import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(PROJECT_ROOT)

from src.extract import fetch_coin_data, fetch_market_data
from src.transform import transform_data
from src.load import load_data_to_database
from src.config import Config

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
import datetime
import pendulum

default_args = {
    "owner": "data_engineering",
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=1),
}

with DAG (
    dag_id='Crypto_ETL_Pipeline',
    tags=["crypto", "etl"],
    default_args= default_args,
    start_date= pendulum.datetime(2026, 3, 11,tz='UTC'),
    description='A Crypto ETL Pipeline Using Airflow',
    # schedule='@hourly',
    schedule='*/5 * * * *',
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=30),
    doc_md="""
    ### Crypto ETL Pipeline

    Pipeline extracts crypto market data from CoinGecko API,
    transforms the data using Polars, and loads it into PostgreSQL.
    """
) as dag:
    
    fetch_coin_task = PythonOperator(
        task_id = "fetch_coin_data",
        python_callable=fetch_coin_data,
        
    )
    
    fetch_market_task = PythonOperator(
        task_id = "fetch_market_data",
        python_callable=fetch_market_data,
        op_args=[fetch_coin_task.output],
    )
    
    
    transform_data_task = PythonOperator(
        task_id="transform_data_task",
        python_callable=transform_data,
        op_args=[fetch_market_task.output],
    )
    
    load_data_to_database_task = PythonOperator(
        task_id = "load_data_to_db",
        python_callable=load_data_to_database,
        op_args=[transform_data_task.output, Config.CRYPTO_TABLE],
    )
    
    fetch_coin_task >> fetch_market_task >>  transform_data_task >> load_data_to_database_task