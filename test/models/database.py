import sqlite3
import os

def initialize_db(db_name='data/university_schedule.db'):
    # Assurez-vous que le dossier existe
    if not os.path.exists('data'):
        os.makedirs('data')

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY,
            room_number TEXT NOT NULL,
            capacity INTEGER NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            day TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            instructor_id INTEGER,
            room_id INTEGER,
            FOREIGN KEY (instructor_id) REFERENCES instructors(id),
            FOREIGN KEY (room_id) REFERENCES rooms(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS instructors (
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            office_hours TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
