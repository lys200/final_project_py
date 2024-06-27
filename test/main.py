from models.room import Room
from models.instructor import Instructor
from models.course import Course
from models.schedule import Schedule
import models.database
def main():
    # Initialiser la base de données
    models.database.initialize_db()

    # Demander à l'utilisateur d'entrer les informations des salles de cours
    room_number = input("Entrez le numéro de la salle: ")
    capacity = int(input("Entrez la capacité de la salle: "))
    room = Room(room_number, capacity)
    room.save_to_db()

    # Demander à l'utilisateur d'entrer les informations des instructeurs
    first_name = input("Entrez le prénom de l'instructeur: ")
    last_name = input("Entrez le nom de famille de l'instructeur: ")
    email = input("Entrez l'email de l'instructeur: ")
    office_hours = input("Entrez les heures de bureau de l'instructeur (facultatif): ")
    instructor = Instructor(first_name, last_name, email, office_hours)
    instructor.save_to_db()

    # Demander à l'utilisateur d'entrer les informations des cours
    course_name = input("Entrez le nom du cours: ")
    day = input("Entrez le jour du cours: ")
    start_time = input("Entrez l'heure de début du cours (HH:MM): ")
    end_time = input("Entrez l'heure de fin du cours (HH:MM): ")

    # Associer l'instructeur et la salle de cours
    instructor_id = instructor.get_id() # Fonction pour obtenir l'ID de l'instructeur
    room_id = room.get_id() # Fonction pour obtenir l'ID de la salle de cours

    course = Course(course_name, day, start_time, end_time, instructor_id, room_id)
    course.save_to_db()

    # Afficher l'emploi du temps
    schedule = Schedule()
    schedule.display_schedule()

if __name__ == "__main__":
    main()
