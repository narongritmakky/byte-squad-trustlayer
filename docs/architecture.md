# Architecture

This document describes the high-level architecture of the Byte Squad TrustLayer system. The platform is composed of four containerised services — `api`, `judge-worker`, `docs-sync`, and `db` — orchestrated via Docker Compose. The `api` service exposes an HTTP interface, `judge-worker` applies Trust Layer rules asynchronously, `docs-sync` keeps reference documentation in sync, and `db` provides a PostgreSQL + pgvector persistence layer. Detailed design decisions for each service are captured in their respective docs under `docs/services/`.
