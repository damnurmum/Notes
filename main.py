from database.notemanage import Note, getnotes, searchnote
from database.databasemain import createtables
import asyncio

asyncio.run(createtables())

async def selectnote():
    answer = input("\nВыберите вашу заметку, чтобы посмотреть содержание заметки/удалить заметку: ")

    if answer.isdigit():
        note = Note(answer)
        note_data = await note.get()
        if note_data is not None:
            print("\n\nЗаголовок: {note_title}\nСодержание: {note_description}".format(
                note_title = note_data['note_title'], 
                note_description = note_data['note_description']
                ))
                    
            print("[1] - Удалить заметку.\n[2] - Выйти в главное меню")

            answer = str(input("Выберите один из пунктов: "))
            if answer.isdigit():
                if int(answer) == 1:
                    await note.delete()
                    print("\nВы удалили свою заметку")

                else:
                    pass
                    
        else:
            print("\nТакой заметки не найдено!")

async def mynotes():
    notes = await getnotes()

    for note in notes:
        print("[{note_id}] - {note_title}".format(note_id = note['note_id'], note_title = note['note_title']))

    await selectnote()

async def createnote():
    title = input("Введите заголовок заметки - ")
    description = input("Введите содержание заметки - ")

    note = Note()
    await note.create(title, description)

    print("\n\nВаша заметка успешно создана")

async def searchnotes():
    keyword = input("Введите ключевое слово для поиска: ")
    notes = await searchnote(keyword)

    if notes is not None:
        for note in notes:
            print("[{note_id}] - {note_title}".format(note_id = note['note_id'], note_title = note['note_title']))

        answer = input("Введите номер заметки, чтобы посмотеть содержимое.")
        if answer.isdigit():
            note = Note(int(answer))
            note_data = await note.get()
            print("\n\nЗаголовок: {note_title}\n\nСодержание: {note_description}".format(
                note_title = note_data['note_title'], 
                note_description = note_data['note_description']
            ))

async def main():
    while True:
        print('\n\n[1] Мои заметки\n[2] Создать заметку\n[3] Найти заметку\n\n')

        answer = int(input("Выберите один из пунктов, для управления вашими заметками:"))
        
        if answer == 1:
            await mynotes()            

        elif answer == 2:
            await createnote()

        elif answer == 3:
            await searchnotes()
  
asyncio.run(main())