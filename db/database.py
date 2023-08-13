import sqlite3


connection = sqlite3.connect('GPT-database.db')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        email TEXT NOT NULL
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS uploads (
        id INTEGER PRIMARY KEY,
        uid TEXT NOT NULL,
        filename TEXT NOT NULL,
        upload_time DATETIME NOT NULL,
        finish_time DATETIME NOT NULL,
        status TEXT,
        FOREIGN KEY (id) REFERENCES users (id)
    )""")

connection.commit()
