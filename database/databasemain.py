import sqlite3
import pathlib
from typing import Tuple

# Path to the SQLite database file (in the same folder)
DB_PATH = pathlib.Path(__file__).parent / "base.db"


def connectdb() -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    """Return a (connection, cursor) tuple for the SQLite database.

    This function opens a new connection each time it is called. Callers
    must close the connection after performing DB operations.
    """

    db = sqlite3.connect(str(DB_PATH))  # open (or create) the DB file
    sql = db.cursor()  # create a cursor for executing statements
    return db, sql


def createtables() -> None:
    """Create the `notes` table if it doesn't already exist.

    This is safe to call multiple times (uses IF NOT EXISTS).
    """

    db, sql = connectdb()
    # Create a simple notes table: id, title, description
    sql.execute(
        """CREATE TABLE IF NOT EXISTS notes (
        note_id INTEGER PRIMARY KEY AUTOINCREMENT,
        note_title TEXT,
        note_description TEXT
    )"""
    )
    db.commit()  # persist changes
    db.close()  # close connection