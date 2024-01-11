import sqlite3
import Client
def createDataBaseFile():
    dataBaseFile = Client.config["username"] + '.db'
    return dataBaseFile

dataBaseFile = createDataBaseFile()

def initDataBase():
    connection = sqlite3.connect(f'./database/{dataBaseFile}')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MailBox (
            status TEXT NOT NULL,
            [from] TEXT NOT NULL,
            subject TEXT NOT NULL,
            [to] TEXT NOT NULL,
            cc TEXT NOT NULL,
            content TEXT NOT NULL,
            fileNames TEXT NOT NULL,
            fileContents TEXT NOT NULL,
            id INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Inbox (
            status TEXT NOT NULL,
            [from] TEXT NOT NULL,
            subject TEXT NOT NULL,
            [to] TEXT NOT NULL,
            cc TEXT NOT NULL,
            content TEXT NOT NULL,
            fileNames TEXT NOT NULL,
            fileContents TEXT NOT NULL,
            id INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Important (
            status TEXT NOT NULL,
            [from] TEXT NOT NULL,
            subject TEXT NOT NULL,
            [to] TEXT NOT NULL,
            cc TEXT NOT NULL,
            content TEXT NOT NULL,
            fileNames TEXT NOT NULL,
            fileContents TEXT NOT NULL,
            id INTEGER NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Project (
            status TEXT NOT NULL,
            [from] TEXT NOT NULL,
            subject TEXT NOT NULL,
            [to] TEXT NOT NULL,
            cc TEXT NOT NULL,
            content TEXT NOT NULL,
            fileNames TEXT NOT NULL,
            fileContents TEXT NOT NULL,
            id INTEGER NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Work (
            status TEXT NOT NULL,
            [from] TEXT NOT NULL,
            subject TEXT NOT NULL,
            [to] TEXT NOT NULL,
            cc TEXT NOT NULL,
            content TEXT NOT NULL,
            fileNames TEXT NOT NULL,
            fileContents TEXT NOT NULL,
            id INTEGER NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Spam (
            status TEXT NOT NULL,
            [from] TEXT NOT NULL,
            subject TEXT NOT NULL,
            [to] TEXT NOT NULL,
            cc TEXT NOT NULL,
            content TEXT NOT NULL,
            fileNames TEXT NOT NULL,
            fileContents TEXT NOT NULL,
            id INTEGER NOT NULL
        )
    ''')

    connection.commit()
    connection.close()