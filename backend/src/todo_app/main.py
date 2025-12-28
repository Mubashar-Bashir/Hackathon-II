import sys
from .ui.cli import app as cli_app
from .ui.interactive_cli import main as interactive_main


def main():
    """Main entry point for the application."""
    # Check if arguments were provided
    if len(sys.argv) > 1:
        # Use command-line interface
        cli_app()
    else:
        # Use interactive interface
        interactive_main()


if __name__ == "__main__":
    main()