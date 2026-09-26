from fastapi import APIRouter, HTTPException
from ...core.config import PipelineConfig, StepConfig
from ...core.pipeline import Pipeline
from ..schemas import PipelineCreate, PipelineOut

router = APIRouter(prefix="/pipelines", tags=["pipelines"])

_registered_pipelines: dict = {}

@router.post("/", response_model=PipelineOut)
def register_pipeline(payload: PipelineCreate):
    steps = [
        StepConfig(plugin_type=s.plugin_type, plugin_name=s.plugin_name, params=s.params)
        for s in payload.steps
    ]
    config = PipelineConfig(
        name=payload.name, steps=steps,
        max_retries=payload.max_retries, timeout_seconds=payload.timeout_seconds,
    )
    _registered_pipelines[payload.name] = config
    return PipelineOut(name=payload.name, step_count=len(steps))

@router.get("/{name}", response_model=PipelineOut)
def get_pipeline(name: str):
    config = _registered_pipelines.get(name)
    if not config:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return PipelineOut(name=config.name, step_count=len(config.steps))

@router.post("/{name}/run")
def run_pipeline(name: str):
    config = _registered_pipelines.get(name)
    if not config:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    pipeline = Pipeline(config)
    context = pipeline.run()
    return {
        "pipeline_name": name,
        "has_errors": context.has_errors(),
        "errors": context.errors,
    }
