import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               age INTEGER NOT NULL,
               grade TEXT NOT NULL
               )
""")

conn.commit()
conn.close()
print('students.db created and table set up!')