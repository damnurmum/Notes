"""Command-line interface (CLI) for Notes application.

This module contains synchronous functions used by `main.py` to show
menus and perform note operations.
"""

from database.notemanage import Note, getnotes, searchnote
from database.databasemain import createtables
from ui import title, menu, prompt, info, error, note_line


def selectnote():
    answer = prompt("Enter note ID to view or delete: ")

    if not answer.isdigit():
        error("Invalid input, expected a note ID.")
        return

    # load selected note by id
    note = Note(int(answer))
    note_data = note.get()
    if note_data is not None:
        title("View Note")
        # print title and description of the note
        print(f"{note_data['note_title']}\n\n{note_data['note_description']}")

        print()
        print("[1] Delete note    [2] Back")

        # ask for confirmation/action
        answer = prompt("Choose action: ")
        if answer.isdigit() and int(answer) == 1:
            note.delete()  # delete the note from DB
            info("Note deleted.")
    else:
        error("Note not found!")


def mynotes():
    # show list of user's notes
    notes = getnotes()
    title("My Notes")
    if not notes:
        info("No notes found.")
        return

    for n in notes:
        print(note_line(n))  # formatted single-line per note

    selectnote()  # let user pick one for viewing/deleting


def createnote():
    # create a new note with user-provided title and description
    title('Create Note')
    title_text = prompt("Enter title: ")
    if not title_text.strip():
        error("Title cannot be empty.")
        return
    description = prompt("Enter content: ")

    note = Note()
    note.create(title_text.strip(), description.strip())

    info("Note created successfully.")


def searchnotes():
    # search notes by keyword and let user view a result
    title('Search Notes')
    keyword = prompt("Enter keyword: ")
    notes = searchnote(keyword)

    if notes:
        for n in notes:
            print(note_line(n))

        answer = prompt("Enter note ID to view: ")
        if answer.isdigit():
            note = Note(int(answer))
            note_data = note.get()
            if note_data:
                title('Search Result')
                print(f"{note_data['note_title']}\n\n{note_data['note_description']}")
    else:
        info("No matches found.")


def main():
    # Ensure tables exist before starting the CLI
    createtables()

    # Main input loop
    while True:
        title('Notes — Main Menu')
        menu(["My Notes", "Create Note", "Search Notes"])

        answer = prompt("Choose menu item: ")
        if not answer.isdigit():
            error("Invalid input, enter a number.")
            continue

        choice = int(answer)

        if choice == 0:
            info("Goodbye.")
            break
        elif choice == 1:
            mynotes()
        elif choice == 2:
            createnote()
        elif choice == 3:
            searchnotes()
        else:
            error("Invalid menu item.")
