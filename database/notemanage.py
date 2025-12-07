"""Database helpers for notes (synchronous, sqlite3).

Provides convenience functions `getnotes`, `searchnote` and a `Note`
class with basic CRUD operations.
"""

from database.databasemain import connectdb
from typing import List, Optional, Dict


def getnotes() -> Optional[List[Dict]]:
    """Return a list of all notes or None when no rows exist."""

    db, sql = connectdb()  # open connection and cursor
    sql.execute("SELECT * FROM notes")  # query all notes
    result = sql.fetchall()  # fetch rows
    db.close()  # close DB connection

    if result:
        # Map rows to dictionaries for easier consumption by CLI
        return [
            {"note_id": r[0], "note_title": r[1], "note_description": r[2]} for r in result
        ]

    return None


def searchnote(keyword: str) -> Optional[List[Dict]]:
    """Search notes by keyword in title or description and return matching rows."""

    db, sql = connectdb()
    sql.execute(
        "SELECT note_id, note_title FROM notes WHERE note_title LIKE ? OR note_description LIKE ?",
        (f"%{keyword}%", f"%{keyword}%"),
    )
    result = sql.fetchall()
    db.close()

    if result:
        return [{"note_id": r[0], "note_title": r[1]} for r in result]

    return None


class Note:
    """Simple synchronous Note model with create/get/delete methods."""

    def __init__(self, note_id: int = None):
        # Store the current note id (optional)
        self.note_id = note_id

    def create(self, note_title: str, note_description: str) -> None:
        # Insert a new row and save lastrowid to self.note_id
        db, sql = connectdb()
        sql.execute(
            "INSERT INTO notes (note_title, note_description) VALUES (?, ?)",
            (str(note_title), str(note_description)),
        )
        self.note_id = sql.lastrowid
        db.commit()
        db.close()

    def delete(self) -> bool:
        # Delete the note identified by self.note_id
        if self.note_id is None:
            return False
        db, sql = connectdb()
        sql.execute("DELETE FROM notes WHERE note_id = ?", (self.note_id,))
        db.commit()
        db.close()
        return True

    def get(self) -> Optional[Dict]:
        # Retrieve a single note by id and return it as a dict
        if self.note_id is None:
            return None
        db, sql = connectdb()
        sql.execute("SELECT * FROM notes WHERE note_id = ?", (self.note_id,))
        note = sql.fetchone()
        db.close()
        if note:
            return {"note_id": note[0], "note_title": note[1], "note_description": note[2]}
        return None

