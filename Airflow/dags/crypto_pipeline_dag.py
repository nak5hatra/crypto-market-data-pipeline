from airflow import DAG
from airflow.operators.python import PythonOperator
import datetime
import pendulum

from src.extract import fetch_coin_data, fetch_market_data
from src.transform import transform_data
from src.load import load_dim_coin, load_fact_crypto

default_args = {
    "owner": "data_engineering",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": datetime.timedelta(minutes=2),
}

with DAG(
    dag_id="crypto_etl_pipeline",
    default_args=default_args,
    start_date=pendulum.datetime(2026, 3, 11, tz="UTC"),
    schedule="@hourly",
    catchup=False,
    tags=["crypto", "etl"],
) as dag:

    extract_coin = PythonOperator(
        task_id="extract_coin_data",
        python_callable=fetch_coin_data,
    )

    extract_market = PythonOperator(
        task_id="extract_market_data",
        python_callable=fetch_market_data,
    )

    transform = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
        op_args=["/opt/airflow/data/raw/market_data.json"], 
    )

    load_dim = PythonOperator(
        task_id="load_dim_coin",
        python_callable=load_dim_coin,
        op_args=["/opt/airflow/data/staging/dim_coin.parquet"],
    )

    load_fact = PythonOperator(
        task_id="load_fact_crypto",
        python_callable=load_fact_crypto,
        op_args=["/opt/airflow/data/staging/fact_crypto_price.parquet"],
    )

    extract_coin >> extract_market >> transform >> [load_dim, load_fact]