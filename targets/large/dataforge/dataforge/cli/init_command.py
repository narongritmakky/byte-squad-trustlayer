import json
import os

TEMPLATE = {
    "name": "my_pipeline",
    "steps": [
        {"plugin_type": "connector", "plugin_name": "csv", "params": {"file_path": "input.csv"}},
        {"plugin_type": "exporter", "plugin_name": "json", "params": {"file_path": "output.json"}},
    ],
    "max_retries": 3,
    "timeout_seconds": 300,
}

def cmd_init(args):
    output_path = args.output or "pipeline.json"
    if os.path.exists(output_path):
        print(f"Error: {output_path} already exists")
        return
    with open(output_path, "w") as f:
        json.dump(TEMPLATE, f, indent=2)
    print(f"Created pipeline template at {output_path}")
