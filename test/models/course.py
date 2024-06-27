import sqlite3

class Course:
    def __init__(self, name, day, start_time, end_time, instructor_id=None, room_id=None):
        self.name = name
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.instructor_id = instructor_id
        self.room_id = room_id

    def save_to_db(self, db_name='data/university_schedule.db'):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO courses (name, day, start_time, end_time, instructor_id, room_id) VALUES (?, ?, ?, ?, ?, ?)', 
                       (self.name, self.day, self.start_time, self.end_time, self.instructor_id, self.room_id))
        conn.commit()
        conn.close()

    def __str__(self):
        return f"{self.name} - {self.day} {self.start_time}-{self.end_time}"
