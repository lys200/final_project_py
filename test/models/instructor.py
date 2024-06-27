import sqlite3
from .person import Person

class Instructor(Person):
    def __init__(self, first_name, last_name, email, office_hours=None):
        super().__init__(first_name, last_name, email)
        self.office_hours = office_hours

    def save_to_db(self, db_name='data/university_schedule.db'):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO instructors (first_name, last_name, email, office_hours) VALUES (?, ?, ?, ?)', 
                       (self.first_name, self.last_name, self.email, self.office_hours))
        conn.commit()
        conn.close()

    def get_id(self, db_name='data/university_schedule.db'):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM instructors WHERE email = ?', (self.email,))
        instructor_id = cursor.fetchone()[0]
        conn.close()
        return instructor_id

    def contact_info(self):
        info = super().contact_info()
        if self.office_hours:
            info += f", Office Hours: {self.office_hours}"
        return info

    def __str__(self):
        return f"Instructor: {super().__str__()}"
