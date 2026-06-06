import sqlite3

conn = sqlite3.connect('students.db')

conn.execute('''
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    course TEXT,
    email TEXT
)
''')

conn.commit()
conn.close()

print("Database Created Successfully")