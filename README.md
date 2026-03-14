# Crypto Market Data Pipeline

A production-style **Data Engineering pipeline** that extracts cryptocurrency market data from the CoinGecko API, transforms it using Polars, and loads it into PostgreSQL. The pipeline is orchestrated using Airflow and runs inside a fully containerized Docker environment.

This project demonstrates how modern data pipelines are built using modular ETL design, orchestration, and containerization.

---

# Architecture

```
            CoinGecko API
                  │
                  ▼
            Data Extraction
               (Python)
                  │
                  ▼
            Data Transformation
                (Polars)
                  │
                  ▼
              PostgreSQL
              Data Storage
                  │
                  ▼
            Airflow Scheduler
        (Pipeline Orchestration)
```

---

# Tech Stack

1. Python
2. Polars
3. PostgreSQL
4. Apache Airflow
5. Docker
6. CoinGecko API

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
│   ├── extraction_dumps/
│   └── transformed_dump/
│
├── sql/
│   └── schema.sql
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

### Folder Explanation

**Airflow/**:
Contains DAG definitions used to orchestrate and schedule the data pipeline.

**data/**:
Stores intermediate pipeline outputs such as raw extracted data and transformed datasets.

**sql/**:
Contains SQL schema definitions used to create database tables.

**src/**:
Core pipeline logic including extraction, transformation, and loading modules.

**Dockerfile & docker-compose.yml**
Used to containerize and run the pipeline and Airflow environment.

---

# Pipeline Workflow

1. Fetch list of available cryptocurrencies from the CoinGecko API.
2. Retrieve market data.
3. Transform raw API data using Polars.
4. Store cleaned data into PostgreSQL tables.
5. Airflow schedules and orchestrates the pipeline execution.

---

# Features

1. Modular ETL pipeline design
2. API-based data ingestion
3. Data transformation using Polars
4. PostgreSQL data storage
5. Airflow DAG orchestration
6. Fully containerized environment using Docker

---

# Setup Instructions

### 1 Clone the repository

```
git clone https://github.com/nak5hatra/crypto-market-data-pipeline.git
cd crypto-market-data-pipeline
```

---

### 2 Create environment variables

Create a `.env` file and configure:

```
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=crypto_db
```

---

### 3 Start the environment

```
docker compose up --build
```

This will start:

* PostgreSQL
* Airflow
* Pipeline environment

---

# Running the Pipeline

Once the containers are running:

1. Open Airflow UI

```
http://localhost:8080
```

2. Enable the DAG:

```
crypto_pipeline_dag
```

3. Trigger the pipeline.

Airflow will execute the full ETL workflow.

---

# Example Data Collected

The pipeline collects market metrics such as:

* Coin ID
* Symbol
* Current Price
* Market Cap
* 24h Price Change
* Trading Volume

---


# Learning Outcomes

This project demonstrates practical experience with:

* Building modular ETL pipelines
* API-based data ingestion
* Data transformation at scale
* Pipeline orchestration using Airflow
* Containerized data engineering environments

---

# Author

Nakshatra Sharma

Data Analyst transitioning into Data Engineering.
