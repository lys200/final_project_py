import sqlite3

class Schedule:
    def __init__(self):
        pass

    def display_schedule(self, db_name='data/university_schedule.db'):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT rooms.room_number, courses.name, courses.day, courses.start_time, courses.end_time, instructors.first_name, instructors.last_name
            FROM courses
            JOIN rooms ON courses.room_id = rooms.id
            LEFT JOIN instructors ON courses.instructor_id = instructors.id
        ''')
        rows = cursor.fetchall()
        for row in rows:
            print(f"Salle {row[0]}: {row[1]} - {row[2]} {row[3]}-{row[4]}, Instructor: {row[5]} {row[6]}")
        conn.close()
