from ..core.config import PipelineConfig
from ..core.exceptions import PipelineConfigError

def cmd_validate(args):
    try:
        config = PipelineConfig.from_file(args.config_path)
        print(f"✓ Pipeline '{config.name}' is valid ({len(config.steps)} steps)")
    except PipelineConfigError as exc:
        print(f"✗ Invalid pipeline config: {exc}")
