import sqlite3

DATABASE = 'data/accounts.db'

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL,
    Email TEXT NOT NULL UNIQUE,
    Company TEXT,
    Role TEXT,
    RoleInCompany TEXT
)
''')

conn.commit()
conn.close()