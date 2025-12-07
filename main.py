"""Entry point for Notes CLI application.

This module runs the `main()` function from `cli.py` when executed
as a script.
"""

from cli import main


if __name__ == "__main__":
    # Run the synchronous CLI main loop and handle Ctrl+C gracefully.
    try:
        main()
    except KeyboardInterrupt:
        # Print a friendly exit message on keyboard interrupt.
        print("\nGoodbye.")