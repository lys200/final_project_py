import sqlite3

class Room:
    def __init__(self, room_number, capacity):
        self.room_number = room_number
        self.capacity = capacity

    def save_to_db(self, db_name='data/university_schedule.db'):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO rooms (room_number, capacity) VALUES (?, ?)', 
                       (self.room_number, self.capacity))
        conn.commit()
        conn.close()

    def get_id(self, db_name='data/university_schedule.db'):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM rooms WHERE room_number = ?', (self.room_number,))
        room_id = cursor.fetchone()[0]
        conn.close()
        return room_id

    def __str__(self):
        return f"Salle {self.room_number} (Capacité: {self.capacity})"
