import sqlite3

conn = sqlite3.connect("hangouthub.db")
cursor = conn.cursor()

# Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Events Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT NOT NULL,
    description TEXT,
    date TEXT,
    time TEXT,
    location TEXT,
    category TEXT,
    created_at TEXT
)
""")

conn.commit()

print("Users and Events tables created successfully!")

conn.close()