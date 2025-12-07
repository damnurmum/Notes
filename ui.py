"""Terminal UI helpers.

Provides simple wrappers for colored output and nicely formatted
menus. Falls back to uncolored output if `colorama` is not available.
"""

try:
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
except Exception:
    # colorama not installed — fallback to empty attributes
    class _Empty:
        pass

    # Simple empty placeholders for color constants to keep API stable
    Fore = Back = Style = _Empty()
    for name in ['BLACK','RED','GREEN','YELLOW','BLUE','MAGENTA','CYAN','WHITE','RESET']:
        setattr(Fore, name, '')
        setattr(Back, name, '')
        setattr(Style, name, '')

import shutil


def term_width():
    """Return terminal width (fallback to 80)."""
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return 80


def title(text: str):
    """Print a centered title block across the terminal width."""
    width = term_width()
    line = "=" * width
    print(getattr(Fore, 'CYAN', '') + line)
    print(getattr(Fore, 'CYAN', '') + text.center(width))
    print(getattr(Fore, 'CYAN', '') + line)


def menu(items):
    """Print a numbered menu with nice formatting."""
    print()
    for i, item in enumerate(items, start=1):
        print(getattr(Fore, 'YELLOW', '') + f"[{i}] " + getattr(Fore, 'WHITE', '') + item)
    print(getattr(Fore, 'YELLOW', '') + "[0] " + getattr(Fore, 'WHITE', '') + "Exit")


def info(msg: str):
    """Print an informational message (green)."""
    print(getattr(Fore, 'GREEN', '') + msg)


def error(msg: str):
    """Print an error message (red)."""
    print(getattr(Fore, 'RED', '') + msg)


def prompt(msg: str) -> str:
    """Prompt the user with a colored prompt and return input string."""
    return input(getattr(Fore, 'MAGENTA', '') + msg + getattr(Fore, 'RESET', ''))


def note_line(note):
    """Return a single formatted line for a note item."""
    return getattr(Fore, 'BLUE', '') + f"[{note['note_id']}] " + getattr(Style, 'BRIGHT', '') + getattr(Fore, 'WHITE', '') + note['note_title']
