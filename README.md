# 🚀 Python ETL Utilities

> **A reusable, metadata-driven ETL framework for building scalable, testable, and observable data pipelines using Python.**

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas)](https://pandas.pydata.org/)
[![Pytest](https://img.shields.io/badge/Tested%20with-Pytest-0A9EDC?logo=pytest)](https://pytest.org/)
[![REST API](https://img.shields.io/badge/Integration-REST%20API-orange)](#module-7--rest-api--incremental-ingestion)
[![Parquet](https://img.shields.io/badge/Storage-Parquet-lightgrey)](#supported-targets)
[![Status](https://img.shields.io/badge/Status-Active%20Development-yellow)](#roadmap)

---

## 📌 Project Overview

**Python ETL Utilities** is a reusable Data Engineering framework designed to solve common ETL requirements without creating a separate Python pipeline for every dataset.

Instead of building:

```text
CustomerJob.py
ProductJob.py
OrderJob.py
TransactionJob.py
```

the framework uses **metadata-driven configuration**:

```text
                    config.yaml
                         │
                         ▼
                  ┌─────────────┐
                  │ ConfigLoader│
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │  ETLRunner  │
                  └──────┬──────┘
                         │
              ┌──────────┼──────────┐
              │          │          │
              ▼          ▼          ▼
            Files      REST API   Database*
              │          │
              └──────────┼──────────┘
                         ▼
                  Data Validation
                         │
                         ▼
                   Transformation
                         │
                         ▼
                       Loading
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
             CSV      Parquet     JSON
                         │
                         ▼
                  Monitoring /
                    Metrics
```

* Database connectors are part of the planned roadmap.

---

# 🎯 Why This Project?

Real-world Data Engineering involves much more than reading a CSV and transforming a DataFrame.

A production ETL framework needs to handle:

* Different source types
* API failures
* Pagination
* Retries
* Schema validation
* Data quality
* Transformation
* Configuration
* Logging
* Monitoring
* Metrics
* Incremental processing
* Watermarks
* Restartability
* Testing
* Error handling

This project brings these capabilities together into a single reusable framework.

---

# 🏗️ Architecture

## Current Architecture

```text
                         ┌─────────────────────┐
                         │    config.yaml      │
                         │   Pipeline Metadata │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    ConfigLoader     │
                         │ Configuration       │
                         │ Validation          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      ETLRunner      │
                         │ Pipeline Execution  │
                         └──────────┬──────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
                ▼                   ▼                   ▼
        ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
        │     CSV      │    │     JSON     │    │   REST API   │
        │    Source    │    │    Source    │    │    Source    │
        └──────┬───────┘    └──────┬───────┘    └──────┬───────┘
               │                   │                   │
               └───────────────────┼───────────────────┘
                                   ▼
                         ┌─────────────────────┐
                         │   Data Validation   │
                         │                     │
                         │ • Required columns  │
                         │ • Null validation   │
                         │ • Duplicate checks  │
                         │ • Primary key       │
                         │ • Email validation  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Transformations   │
                         │                     │
                         │ • Rename            │
                         │ • Trim              │
                         │ • Type conversion   │
                         │ • Dates             │
                         │ • Null handling      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     Data Loader     │
                         └──────────┬──────────┘
                                    │
                   ┌────────────────┼────────────────┐
                   │                │                │
                   ▼                ▼                ▼
                 CSV             JSON            Parquet
                                   
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Monitoring & Metrics│
                         │                     │
                         │ Logs                │
                         │ Execution ID        │
                         │ Record counts       │
                         │ Duration            │
                         │ Audit records       │
                         └─────────────────────┘
```

---

# 🧠 Core Design Principle

The framework follows:

> **Configuration over hard-coded pipeline logic.**

A new pipeline should primarily require metadata changes rather than a new Python class.

Example:

```yaml
pipelines:

  - name: customers
    source:
      type: csv
      path: data/raw/customers.csv

  - name: transactions
    source:
      type: json
      path: data/raw/transactions.json

  - name: api_customers
    source:
      type: api
      url: https://dummyjson.com/users
      records_path: users
```

The same:

```text
ETLRunner
DataLoader
Validator
Transformer
Monitor
```

can process all three.

---

# 🧩 Modules

| Module | Capability                          | Status         |
| ------ | ----------------------------------- | -------------- |
| 1      | REST API Client                     | ✅ Completed    |
| 2      | File Processing                     | ✅ Completed    |
| 3      | Data Quality & Validation           | ✅ Completed    |
| 4      | Transformations                     | ✅ Completed    |
| 5      | Logging & Observability             | ✅ Completed    |
| 6      | Configuration & Metadata-Driven ETL | ✅ Completed    |
| 7      | REST API & Incremental Ingestion    | 🚧 In Progress |
| 8      | ETL Orchestration                   | 📋 Planned     |
| 9      | Advanced Data Quality               | 📋 Planned     |
| 10     | Cloud & Delta Lake                  | 📋 Planned     |
| 11     | Streaming                           | 📋 Planned     |
| 12     | CI/CD & Deployment                  | 📋 Planned     |

---

# 📦 Module 1 — REST API Client

## Features

* HTTP GET
* Session reuse
* Timeout
* Retry
* Exponential backoff
* Custom headers
* Query parameters
* JSON parsing
* Context manager

Example:

```python
from etl_utils.api_client import APIClient

with APIClient() as client:

    response = client.get(
        "https://dummyjson.com/users"
    )

    print(response)
```

## Retry Strategy

Transient errors can be retried:

```text
429  Too Many Requests
500  Internal Server Error
502  Bad Gateway
503  Service Unavailable
504  Gateway Timeout
```

The client uses retry + backoff rather than immediately failing on transient failures.

---

# 📂 Module 2 — File Processing

Supported operations include:

```text
CSV
JSON
```

Utilities include:

```text
validate_file_exists()
read_csv()
write_csv()
read_json()
write_json()
validate_columns()
validate_dataframe_not_empty()
```

Example:

```python
df = read_csv(
    "data/raw/customers.csv"
)
```

---

# 🛡️ Module 3 — Data Quality & Validation

The framework validates incoming data before it reaches the target.

## Validation types

### Required columns

```text
customer_id
email
name
```

### Null validation

```text
customer_id → NOT NULL
email       → NOT NULL
```

### Duplicate validation

```text
customer_id → UNIQUE
```

### Primary key

A primary key should satisfy:

```text
NOT NULL
+
UNIQUE
```

### Email validation

Detect malformed email values.

### Data type validation

Examples:

```text
customer_id      → integer
amount           → float
transaction_date → datetime
```

---

# 🔄 Module 4 — Transformations

Transformations are implemented using a chainable API.

Example:

```python
from etl_utils.transformations import DataTransformer

df = (
    DataTransformer(df)
    .trim_strings(
        ["name", "email"]
    )
    .standardize_strings(
        ["city"]
    )
    .convert_types(
        {"amount": "float64"}
    )
    .rename_columns(
        {
            "created_date": "created_at"
        }
    )
    .result()
)
```

## Supported transformations

```text
rename_columns()
standardize_column_names()
trim_strings()
standardize_strings()
convert_types()
standardize_dates()
fill_nulls()
add_column()
filter_rows()
sort_by()
```

---

# 📊 Module 5 — Logging & Observability

Production ETL systems need visibility into execution.

The framework provides:

```text
Application logs
Execution metrics
Execution IDs
Audit records
Pipeline status
Record counts
Duration
Error details
```

Example:

```python
logger.info(
    "Customer pipeline started"
)

logger.info(
    "Processed %s records",
    len(df)
)
```

---

# 🚨 Exception Hierarchy

The framework provides domain-specific exceptions:

```text
ETLError
│
├── ConfigurationError
├── DataValidationError
├── DataTransformationError
├── DataIngestionError
├── DataLoadingError
└── PipelineExecutionError
```

This makes failures easier to identify and handle.

---

# 📈 ETL Metrics

Each pipeline execution can track:

```text
pipeline_name
execution_id
status
start_time
end_time
duration
records_read
records_processed
records_rejected
error_message
```

Example:

```json
{
  "pipeline_name": "customers",
  "status": "SUCCESS",
  "records_read": 1000,
  "records_processed": 980,
  "records_rejected": 20
}
```

---

# ⚙️ Module 6 — Metadata-Driven ETL

The ETL framework is configured using YAML.

Example:

```yaml
environment: development

defaults:
  log_level: INFO
  error_policy: fail_pipeline

pipelines:

  - name: customers

    enabled: true

    source:
      type: csv
      path: data/raw/customers.csv

    primary_key:
      - customer_id

    quality_rules:

      - type: not_null
        columns:
          - customer_id
          - email

      - type: unique
        columns:
          - customer_id

      - type: email
        column: email

    transformations:

      - type: trim
        columns:
          - name
          - email
          - city
          - country

      - type: uppercase
        columns:
          - status

    target:
      type: csv
      path: data/processed/customers.csv
```

---

# 🌐 Module 7 — REST API & Incremental Ingestion

Module 7 extends the framework with REST API ingestion.

Architecture:

```text
REST API
   │
   ▼
APIClient
   │
   ├── Timeout
   ├── Retry
   └── Backoff
   │
   ▼
APIIngestor
   │
   ├── Response extraction
   ├── Pagination
   └── Incremental ingestion
   │
   ▼
DataFrame
```

---

# 🔢 API Pagination

The framework supports limit/offset pagination.

Example:

```yaml
pagination:

  enabled: true

  type: limit_offset

  page_size: 100
```

Requests conceptually become:

```text
GET ?limit=100&skip=0
GET ?limit=100&skip=100
GET ?limit=100&skip=200
...
```

The ingestion layer continues until no additional records are returned.

---

# 📥 Nested API Responses

Many APIs return:

```json
{
  "users": [
    {
      "id": 1,
      "email": "user@example.com"
    }
  ],
  "total": 100
}
```

Metadata can specify:

```yaml
records_path: users
```

The ingestion layer extracts:

```python
response["users"]
```

and converts the records to a Pandas DataFrame.

---

# ⏱️ Incremental Ingestion

Full ingestion:

```text
Run 1 → 1,000,000
Run 2 → 1,000,000
Run 3 → 1,000,000
```

Incremental ingestion:

```text
Run 1 → Initial load
          │
          ▼
       Watermark T1

Run 2 → Records after T1
          │
          ▼
       Watermark T2

Run 3 → Records after T2
```

Example configuration:

```yaml
incremental:

  enabled: true

  column: updated_at

  watermark_store:
    metadata/watermarks.json
```

---

# 💾 Watermark Store

Watermarks are stored separately from pipeline configuration.

Example:

```json
{
  "customers": "2026-09-30T10:30:00",
  "transactions": "2026-09-30T11:45:00"
}
```

The critical rule is:

```text
Read
 ↓
Validate
 ↓
Transform
 ↓
Load
 ↓
SUCCESS
 ↓
Update watermark
```

Never update the watermark before successful processing.

---

# 🔁 Restartability

If a pipeline fails:

```text
Source
  ↓
Batch 1 → SUCCESS
  ↓
Batch 2 → SUCCESS
  ↓
Batch 3 → FAILURE
```

the checkpoint/watermark must remain at the last safe successful position.

This allows the next execution to restart safely.

---

# 🔐 Idempotency

A production pipeline should be safe to rerun.

The framework's design supports this concept using:

```text
Primary keys
+
Deduplication
+
Watermarks
+
Idempotent target writes
```

The exact implementation depends on the target storage technology.

---

# 🧪 Testing Strategy

The project uses `pytest`.

Run all tests:

```powershell
python -m pytest -v
```

Run Module 7 tests:

```powershell
python -m pytest tests/test_api_ingestion.py tests/test_watermark.py -v
```

The API tests use fake clients rather than relying on a live external API.

Example:

```python
class FakeAPIClient:

    def get(self, endpoint, params=None):

        return {
            "users": [
                {
                    "id": 1,
                    "email": "a@example.com"
                },
                {
                    "id": 2,
                    "email": "b@example.com"
                }
            ]
        }
```

This makes unit tests:

* Fast
* Deterministic
* Reproducible
* Independent of network availability

---

# 📁 Project Structure

```text
python-etl-utilities/
│
├── config/
│   └── config.yaml
│
├── data/
│   ├── raw/
│   │   ├── customers.csv
│   │   └── transactions.json
│   │
│   └── processed/
│
├── metadata/
│   └── watermarks.json
│
├── logs/
│
├── examples/
│   ├── file_processing_example.py
│   ├── data_quality_example.py
│   ├── transformation_example.py
│   ├── monitoring_example.py
│   ├── metadata_driven_etl.py
│   └── api_ingestion_example.py
│
├── src/
│   └── etl_utils/
│       ├── __init__.py
│       ├── api_client.py
│       ├── api_ingestion.py
│       ├── config_loader.py
│       ├── data_loader.py
│       ├── data_validator.py
│       ├── transformations.py
│       ├── logger.py
│       ├── exceptions.py
│       ├── metrics.py
│       ├── pipeline_monitor.py
│       ├── watermark.py
│       └── etl_runner.py
│
├── tests/
│   ├── test_api_client.py
│   ├── test_api_ingestion.py
│   ├── test_file_utils.py
│   ├── test_data_validator.py
│   ├── test_transformations.py
│   ├── test_logger.py
│   ├── test_metrics.py
│   ├── test_pipeline_monitor.py
│   ├── test_config_loader.py
│   ├── test_data_loader.py
│   ├── test_etl_runner.py
│   └── test_watermark.py
│
├── pyproject.toml
├── README.md
└── .gitignore
```

---

# 🛠️ Installation

## 1. Clone the repository

```powershell
git clone <your-github-repository-url>
```

## 2. Enter the project

```powershell
cd python-etl-utilities
```

## 3. Create virtual environment

```powershell
python -m venv venv
```

## 4. Activate environment

```powershell
.\venv\Scripts\Activate.ps1
```

## 5. Install project

```powershell
python -m pip install -e ".[dev]"
```

## 6. Install additional dependencies

```powershell
python -m pip install pyyaml pyarrow
```

---

# ▶️ Running the Examples

## File processing

```powershell
python examples/file_processing_example.py
```

## Data validation

```powershell
python examples/data_quality_example.py
```

## Transformations

```powershell
python examples/transformation_example.py
```

## Monitoring

```powershell
python examples/monitoring_example.py
```

## Metadata-driven ETL

```powershell
python examples/metadata_driven_etl.py
```

## REST API ingestion

```powershell
python examples/api_ingestion_example.py
```

---

# 🔍 Example End-to-End Pipeline

```text
                   CONFIGURATION
                        │
                        ▼
                  ConfigLoader
                        │
                        ▼
                    ETLRunner
                        │
                        ▼
               ┌────────────────┐
               │ Source Ingest  │
               └───────┬────────┘
                       │
                       ▼
               ┌────────────────┐
               │ Data Validation│
               └───────┬────────┘
                       │
                       ▼
               ┌────────────────┐
               │ Transformation │
               └───────┬────────┘
                       │
                       ▼
               ┌────────────────┐
               │  Data Loading  │
               └───────┬────────┘
                       │
                       ▼
               ┌────────────────┐
               │ Metrics/Audit  │
               └────────────────┘
```

---

# 📊 Data Flow Example

For a customer API:

```text
DummyJSON API
     │
     ▼
GET /users
     │
     ▼
Pagination
     │
     ▼
JSON response
     │
     ▼
records_path = users
     │
     ▼
Pandas DataFrame
     │
     ▼
Required column validation
     │
     ▼
Null validation
     │
     ▼
Duplicate validation
     │
     ▼
String standardization
     │
     ▼
Parquet
     │
     ▼
Metrics + Logs
```

---

# 🧱 Production Design Decisions

## 1. Separate ingestion from transformation

Bad design:

```text
API call
+
validation
+
transformation
+
loading
```

inside one large function.

Better:

```text
APIClient
   ↓
APIIngestor
   ↓
Validator
   ↓
Transformer
   ↓
DataLoader
```

This improves maintainability and testing.

---

## 2. Metadata-driven execution

Instead of creating one class per dataset, metadata defines:

```text
source
primary key
quality rules
transformations
target
incremental strategy
```

---

## 3. Reusable API client

The API client handles common HTTP concerns:

```text
Retry
Timeout
Headers
Connection reuse
HTTP errors
```

Individual pipelines should not duplicate this logic.

---

## 4. Fail fast on critical data-quality issues

Critical validation failures should prevent bad data from being loaded.

Examples:

```text
Missing primary key
Duplicate primary key
Required field NULL
Invalid schema
```

---

## 5. Update watermark only after success

This protects incremental pipelines from accidentally skipping unprocessed data.

---

# 🎓 Data Engineering Concepts Demonstrated

This project provides practical experience with:

```text
ETL / ELT
REST APIs
HTTP
JSON
CSV
Parquet
Pandas
DataFrames
Data Quality
Schema Validation
Primary Keys
Duplicates
Data Transformation
Configuration Management
Metadata-Driven Architecture
Logging
Monitoring
Metrics
Audit Logging
Retries
Exponential Backoff
Pagination
Incremental Processing
Watermarks
Checkpoints
Restartability
Idempotency
Unit Testing
```

---

# 💼 Interview-Relevant Topics

This project can be used to discuss common Data Engineering interview scenarios.

### API failures

**Question:** How do you handle transient API failures?

```text
Timeout
+
Retry
+
Exponential Backoff
+
HTTP Status Handling
+
Logging
```

### Large API datasets

**Question:** How do you ingest millions of API records?

```text
Pagination
+
Batch processing
+
Rate-limit handling
+
Incremental ingestion
+
Checkpointing
```

### Pipeline failure

**Question:** What happens if the pipeline fails halfway?

```text
Preserve last successful checkpoint
+
Retry/restart
+
Deduplicate
+
Idempotent writes
```

### Incremental ingestion

**Question:** What is a watermark?

A watermark identifies the latest successfully processed position in an incremental source.

Examples:

```text
updated_at
event_time
sequence_id
offset
```

---

# 🧪 Quality Gates

Before considering a module complete:

```text
☑ Code implemented
☑ Unit tests added
☑ Error handling implemented
☑ Logging added
☑ Example created
☑ Configuration documented
☑ README updated
```

---

# 🚀 Roadmap

## Module 8 — Production ETL Orchestration

Planned:

```text
Pipeline dependencies
Pipeline stages
Retry policies
Failure policies
Execution policies
Parallel execution
Pipeline dependency graph
```

Architecture:

```text
Pipeline A
    │
    ▼
Pipeline B
    │
    ├──────────► Pipeline C
    │
    ▼
Pipeline D
```

---

## Module 9 — Advanced Data Quality

Planned:

```text
Rule engine
DQ score
DQ reports
Rejected-record framework
Business rules
Data profiling
Schema drift detection
```

Example:

```yaml
quality_rules:

  - type: not_null
    columns:
      - customer_id

  - type: unique
    columns:
      - customer_id

  - type: email
    column: email

  - type: range
    column: amount
    min: 0
    max: 100000
```

---

## Module 10 — Cloud & Delta Lake

Planned integration:

```text
Azure Data Lake Storage
        │
        ▼
Azure Databricks
        │
        ▼
Delta Lake
        │
        ▼
Medallion Architecture
```

Target architecture:

```text
             REST API / Files
                    │
                    ▼
                Bronze
                    │
                    ▼
                Silver
                    │
                    ▼
                 Gold
```

---

## Module 11 — Streaming

Planned:

```text
Apache Kafka
Structured Streaming
Event-driven ingestion
Streaming checkpoints
Watermarks
Exactly-once processing
```

Architecture:

```text
Kafka
  │
  ▼
Spark Structured Streaming
  │
  ▼
Validation
  │
  ▼
Transformation
  │
  ▼
Delta Lake
```

---

## Module 12 — CI/CD & Deployment

Planned:

```text
GitHub
   │
   ▼
GitHub Actions
   │
   ├── Unit Tests
   ├── Linting
   ├── Build
   └── Package
          │
          ▼
       Deployment
```

Future deployment options:

```text
Docker
Azure
Databricks
Cloud storage
CI/CD
Monitoring
```

---

# 🌟 Long-Term Architecture

The final goal is a reusable Data Engineering platform:

```text
                         ┌──────────────────┐
                         │ Metadata / YAML  │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  Configuration   │
                         │     Engine       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  ETL Orchestrator│
                         └────────┬─────────┘
                                  │
          ┌───────────────────────┼────────────────────────┐
          │                       │                        │
          ▼                       ▼                        ▼
      REST APIs                 Files                  Databases
          │                       │                        │
          └───────────────────────┼────────────────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Data Quality     │
                         │ & Validation     │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Transformations  │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Storage Layer    │
                         └────────┬─────────┘
                                  │
                ┌─────────────────┼─────────────────┐
                ▼                 ▼                 ▼
              Parquet           Delta           Database
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Observability    │
                         ├──────────────────┤
                         │ Logs             │
                         │ Metrics          │
                         │ Audit            │
                         │ Alerts            │
                         └──────────────────┘
```

---

# 📌 Portfolio Highlights

This project demonstrates practical implementation of:

### Python

```text
Object-oriented programming
Exception handling
File handling
Type hints
Dataclasses
Logging
Reusable modules
Context managers
```

### Data Engineering

```text
ETL
Data quality
Schema validation
Incremental ingestion
Watermarks
Pagination
Data transformations
Metadata-driven pipelines
```

### API Engineering

```text
REST APIs
HTTP
Retries
Backoff
Timeouts
Pagination
JSON normalization
```

### Software Engineering

```text
Modular architecture
Unit testing
Configuration management
Error handling
Observability
Reusable components
```

---

# 📈 Future Enhancements

The framework will progressively evolve toward:

```text
                    Python ETL Framework
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
         Batch           Streaming         APIs
            │               │               │
            ▼               ▼               ▼
        Pandas/Spark       Kafka          REST
            │               │               │
            └───────────────┼───────────────┘
                            ▼
                     Data Quality
                            │
                            ▼
                      Delta Lake
                            │
                            ▼
                    Azure Databricks
                            │
                            ▼
                    CI/CD + Monitoring
```

---

# 🤝 Contributing

Contributions, improvements, and suggestions are welcome.

Recommended contribution process:

```text
Fork
  ↓
Create feature branch
  ↓
Implement change
  ↓
Add tests
  ↓
Run pytest
  ↓
Commit
  ↓
Push
  ↓
Pull Request
```

---

# 📄 License

This project is intended for educational, portfolio, and demonstration purposes.

---

# 👩‍💻 Author

## Shehnaz Asfi

**Data Engineering | Python | PySpark | Scala | SQL | Azure Databricks**

This repository is part of a hands-on Data Engineering portfolio focused on building reusable, production-style ETL components.

---

# ⭐ If You Find This Project Useful

Feel free to explore the modules, experiment with the framework, and extend it with additional source systems, storage technologies, orchestration, cloud services, and streaming capabilities.
