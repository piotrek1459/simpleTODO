import sqlite3

connection = sqlite3.connect("todo.db")
cursor = connection.cursor()

cursor.execute("""CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    username TEXT,
    hash TEXT)
    """)

cursor.execute("""CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT,
    description TEXT,
    is_complete INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
    )""")


connection.commit()
connection.close()
