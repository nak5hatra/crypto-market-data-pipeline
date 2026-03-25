# Crypto Market Data Pipeline

A production-style **Data Engineering pipeline** that ingests cryptocurrency market data from the CoinGecko API, processes it through a multi-layer ETL architecture, and loads it into a PostgreSQL data warehouse. The pipeline is orchestrated using Apache Airflow and runs in a fully containerized Docker environment.

This project demonstrates real-world data engineering practices including modular pipeline design, data modeling, idempotent processing, and workflow orchestration.

---

# Architecture
![alt text](https://github.com/nak5hatra/crypto-market-data-pipeline/blob/main/images/architecture.png?raw=true)

# Tech Stack

* Python
* Polars
* PostgreSQL
* Apache Airflow
* Docker
* CoinGecko API

---

# Data Modeling

The pipeline follows a **star schema design**:

### Dimension Table: `dim_coin`

* coin_id (Primary Key)
* coin_symbol
* coin_name

### Fact Table: `fact_crypto_price`

* coin_id (Foreign Key)
* price_usd
* market_cap
* total_volume
* volume_marketcap_ratio
* distance_from_ath_pct
* last_updated

This design improves query performance and supports analytical workloads.

---

# Project Structure

```
crypto-market-data-pipeline
│
├── Airflow/
│   └── dags/
│       └── crypto_pipeline_dag.py
│
├── data/
│   ├── raw/
│   └── staging/
│
├── src/
│   ├── config.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── pipeline.py
│   └── utils.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Pipeline Workflow

1. Fetch list of cryptocurrencies from CoinGecko API
2. Extract market data in batches with retry logic
3. Store raw data as JSON
4. Transform data using Polars into structured format
5. Generate fact and dimension tables
6. Store transformed data as Parquet
7. Load data into PostgreSQL with idempotent logic
8. Orchestrate pipeline execution using Airflow

---

# Features

* Modular ETL pipeline architecture
* API-based data ingestion with batching
* Fault-tolerant extraction with retry and exponential backoff
* Data transformation using Polars
* Columnar storage using Parquet
* Data warehouse modeling (fact + dimension tables)
* Idempotent pipeline design (safe re-runs)
* Workflow orchestration using Airflow
* Fully containerized using Docker

---

# Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/nak5hatra/crypto-market-data-pipeline.git
cd crypto-market-data-pipeline
```

---

### 2. Create environment variables

Create a `.env` file:

```
COINGECKO_API_KEY=your_api_key_here
DB_URL=postgresql+psycopg2://user:password@localhost:5432/crypto_db
```

---

### 3. Start the environment

```
docker compose up --build
```

This will start:

* PostgreSQL
* Airflow
* Pipeline environment

---

# Running the Pipeline

1. Open Airflow UI

```
http://localhost:8080
```

2. Enable the DAG

```
crypto_etl_pipeline
```

3. Trigger the pipeline

Airflow will execute the full ETL workflow.

---

# Key Learnings

* Designed a scalable and modular ETL pipeline
* Implemented star schema data modeling
* Built idempotent pipelines to handle reprocessing
* Handled API rate limits using retry and exponential backoff
* Used Polars for high-performance data transformation
* Orchestrated workflows using Airflow
* Containerized data pipelines using Docker

---

# Author

Nakshatra Sharma

Data Analyst transitioning into Data Engineering.
