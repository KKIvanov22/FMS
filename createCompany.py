import sqlite3

DATABASE = 'data/accounts.db'

def create_companies_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    ''')

    conn.commit()
    conn.close()

def register_company(name):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('INSERT INTO Companies (name) VALUES (?)', (name,))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_companies_table()
    company_name = input("Enter the name of the company: ")
    register_company(company_name)
    print(f"Company '{company_name}' registered successfully.")