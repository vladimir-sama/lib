import os, sqlite3, datetime, shutil
from app import database_path, current_directory

def backup_database() -> None:
    destination : str = 'library_bak_%s' % datetime.datetime.now().strftime('%Y_%m_%d')
    shutil.copy(database_path, os.path.join(current_directory, ))

def initialize_database() -> None:
    conn : sqlite3.Connection = sqlite3.connect(database_path)
    cursor : sqlite3.Cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            isbn_11 TEXT,
            isbn_13 TEXT,
            title TEXT,
            edition TEXT,
            editor TEXT,
            extension INTEGER,
            authors TEXT,
            location TEXT,
            position TEXT,
            classification TEXT,
            tags TEXT,
            notes TEXT,
            physical_characteristics TEXT,
            language TEXT,
            year INTEGER,
            last_modified INTEGER,
            time_added INTEGER,
            collection TEXT
        )
    ''')
    conn.commit()
    conn.close()