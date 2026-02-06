# 🛒 Store Daily Profit Reporting Pipeline (Airflow + MySQL + Docker)

## 📌 Project Overview

This project implements a **production-grade ETL pipeline** using **Apache Airflow**, **MySQL**, and **Docker** to generate **daily store profit reports** from raw transaction data and automatically **email the reports**.

The pipeline:
- Validates raw data availability
- Cleans and transforms CSV data
- Loads data into MySQL
- Computes daily profits using SQL
- Generates CSV reports
- Emails the reports
- Archives raw input files

---

## 🏗️ Architecture
```
Raw CSV
↓
Airflow DAG
↓
Python Data Cleaning
↓
MySQL (Docker, Persistent Volume)
↓
SQL Aggregations
↓
CSV Reports
↓
Email with Attachments

```
---

## 🐳 Tech Stack

- **Apache Airflow 2.x**
- **MySQL 8.0**
- **PostgreSQL** (Airflow metadata DB)
- **Docker & Docker Compose**
- **Python**
- **SQL**

---

## 📁 Project Structure

```text
docker-airflow-master/
│
├──> dags/
│ └──> store_DAG.py
│
├──> sql_files/
│ ├──> create_table.sql
│ ├──> insert_into_table.sql
│ └──> select_from_table.sql
│
├──> store_files/
│ ├──> raw_store_transactions.csv
│ └──> (generated report files)
│
├──> mysql.cnf
├──> docker-compose-LocalExecutor.yml
└──> README.md

```
---

## 🔄 DAG Workflow

**DAG Name:** `store_dag`  
**Schedule:** `@daily`

### Task Flow

check_file_exists
↓
clean_raw_csv
↓
create_mysql_table
↓
insert_into_table
↓
cleanup_old_reports
↓
select_from_table
↓
move_file1 ─┐
├── send_email → rename_raw
move_file2 ─┘


### Task Description

| Task | Description |
|----|------------|
| `check_file_exists` | Verifies raw CSV exists |
| `clean_raw_csv` | Cleans and standardizes raw data |
| `create_mysql_table` | Creates MySQL table if not exists |
| `insert_into_table` | Loads cleaned CSV into MySQL |
| `cleanup_old_reports` | Deletes old CSV reports |
| `select_from_table` | Generates profit reports using SQL |
| `move_file1 / move_file2` | Renames reports with execution date |
| `send_email` | Emails reports as attachments |
| `rename_raw` | Archives raw input file |

---

## 🧠 Key Design Decisions

- **Airflow Macros (`{{ ds }}`, `{{ ds_nodash }}`)** used instead of `datetime.now()`
- **Idempotent pipeline** (safe to re-run)
- **Persistent MySQL storage** using Docker volumes
- **MySQL `INTO OUTFILE` limitation handled** via cleanup task
- **Airflow Connections UI** used for database credentials

---

## 🛠️ Setup Instructions

### 1️⃣ Start Services

```bash
cd docker-airflow-master
docker compose -f ./docker-compose-LocalExecutor.yml up -d
2️⃣ Create Airflow Admin User
docker exec -it docker-airflow-master-webserver-1 bash
airflow users create \
  --username airflow \
  --password airflow \
  --firstname Airflow \
  --lastname Admin \
  --role Admin \
  --email admin@example.com
3️⃣ Access Airflow UI
http://localhost:8080
Login:

username: airflow
password: airflow
🔐 Airflow Connection Setup
Create a MySQL connection in Admin → Connections:

Field	Value
Connection Id	mysql_conn
Connection Type	MySQL
Host	mysql
Schema	airflow_mysql
Login	root
Password	root
Port	3306
🧪 Database Initialization (One-time)
docker exec -it docker-airflow-master-mysql-1 mysql -u root -proot
CREATE DATABASE airflow_mysql;
📧 Email Reporting
Uses Airflow EmailOperator

Sends daily profit CSV reports as attachments

Fully automated post-success

✅ Final Outcome
End-to-end ETL pipeline

Fully automated daily reporting

Restart-safe and production-ready

Clean DAG design following Airflow best practices

🎯 Key Learnings
Always use Airflow macros for dates

Persist databases using Docker volumes

MySQL SELECT INTO OUTFILE is write-once

Idempotency is critical in data pipelines

Airflow Connections override environment variables

🚀 Future Improvements
Convert to TaskFlow API

Add data quality checks

Add SLA alerts

Move SQL OUTFILE logic to Python

Parameterize email recipients

👤 Author
Navaneeth Rao T
Data Engineer
Apache Airflow | SQL | Docker | Python
