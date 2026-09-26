from fastapi import FastAPI
from .routers import pipelines, runs, plugins, health
from ..monitoring.logger_config import configure_logging

configure_logging(level="INFO")

app = FastAPI(
    title="DataForge",
    description="Plugin-based ETL pipeline framework",
    version="1.0.0",
)

app.include_router(health.router)
app.include_router(pipelines.router)
app.include_router(runs.router)
app.include_router(plugins.router)
