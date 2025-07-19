from src.main import run
import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(
        description="Multitasking Coding Agent",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "prompt",
        type=str,
        help="The prompt for the agent.\n"
             "Example: 'Create a simple Flask app with a homepage.'"
    )
    parser.add_argument(
        "--project-path",
        type=str,
        default=".",
        help="The path to the project directory where the agent will work.\n"
             "Defaults to the current directory ('.').\n"
    )
    
    args = parser.parse_args()
    path = os.path.abspath(args.project_path)

    # Create the directory if it doesn't exist
    if not os.path.exists(path):
        print(f"Error: Project directory '{path}' does not exist.", file=sys.stderr)
        sys.exit(1)
    elif not os.path.isdir(path):
        print(f"Error: '{path}' exists but is not a directory.", file=sys.stderr)
        sys.exit(1)

    try:
        run(args.prompt, path)
    except Exception as e:
        print(f"An error occurred during agent execution: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()