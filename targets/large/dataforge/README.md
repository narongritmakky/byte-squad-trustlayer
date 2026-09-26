# DataForge

A plugin-based ETL/data-pipeline framework built on FastAPI and SQLAlchemy.
Compose pipelines from interchangeable connectors, transformers, validators,
and exporters — all registered through a central plugin registry.

## Architecture

    Connector -> Transformer(s) -> Validator(s) -> Exporter

Each stage is a plugin registered in `core/registry.py`. Pipelines are
defined declaratively as JSON config and executed by `core/pipeline.py`.

## Features
- 15 built-in connectors (CSV, Postgres, S3, Kafka, MongoDB, REST API, etc.)
- 15 built-in transformers (filter, join, aggregate, pivot, normalize, etc.)
- 8 built-in validators (null check, regex, uniqueness, outlier detection, etc.)
- 8 built-in exporters (CSV, Parquet, Excel, database, webhook, etc.)
- Cron-based scheduler with background worker pool
- REST API for registering and triggering pipelines
- CLI for running/validating pipelines locally

## Setup

    pip install -r requirements.txt
    uvicorn dataforge.api.app:app --reload

## CLI Usage

    python -m dataforge.cli init --output my_pipeline.json
    python -m dataforge.cli validate my_pipeline.json
    python -m dataforge.cli run my_pipeline.json

## Running Tests

    pytest

## License
MIT — see LICENSE file.
