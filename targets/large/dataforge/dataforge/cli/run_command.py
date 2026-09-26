from ..core.config import PipelineConfig
from ..core.pipeline import Pipeline
from ..core.exceptions import PipelineConfigError
from ..utils.logger import get_logger

logger = get_logger("dataforge.cli")

def cmd_run(args):
    try:
        config = PipelineConfig.from_file(args.config_path)
    except PipelineConfigError as exc:
        logger.error(f"Failed to load config: {exc}")
        return

    pipeline = Pipeline(config)
    context = pipeline.run()

    if context.has_errors():
        logger.warning(f"Pipeline '{config.name}' completed with {len(context.errors)} errors")
        for err in context.errors:
            logger.warning(f"  - {err['step']}: {err['error']}")
    else:
        logger.info(f"Pipeline '{config.name}' completed successfully")
