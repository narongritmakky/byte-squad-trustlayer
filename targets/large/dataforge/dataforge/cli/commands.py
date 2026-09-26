import argparse
from .run_command import cmd_run
from .validate_command import cmd_validate
from .init_command import cmd_init

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dataforge")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a pipeline from a config file")
    run_parser.add_argument("config_path", type=str)
    run_parser.set_defaults(func=cmd_run)

    validate_parser = subparsers.add_parser("validate", help="Validate a pipeline config file")
    validate_parser.add_argument("config_path", type=str)
    validate_parser.set_defaults(func=cmd_validate)

    init_parser = subparsers.add_parser("init", help="Create a new pipeline config template")
    init_parser.add_argument("--output", type=str, default=None)
    init_parser.set_defaults(func=cmd_init)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
