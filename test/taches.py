import sqlite3
from datetime import datetime

# Connexion à la base de données SQLite
conn = sqlite3.connect('taches.db')
cursor = conn.cursor()

# Création de la table des tâches
cursor.execute('''
CREATE TABLE IF NOT EXISTS taches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    jour TEXT NOT NULL,
    heure_debut TEXT NOT NULL,
    heure_fin TEXT NOT NULL
)
''')
conn.commit()

def verifier_conflit(jour, heure_debut, heure_fin):
    """
    Vérifie si une tâche existe déjà dans l'intervalle de temps donné.

    :param jour: Jour de la tâche (e.g., 'lundi')
    :param heure_debut: Heure de début de la tâche (e.g., '10:00')
    :param heure_fin: Heure de fin de la tâche (e.g., '12:00')
    :return: True si un conflit est détecté, False sinon
    """
    query = '''
    SELECT 1 FROM taches
    WHERE jour = ?
    AND (
        (heure_debut <= ? AND heure_fin > ?)
        OR (heure_debut < ? AND heure_fin >= ?)
        OR (heure_debut >= ? AND heure_fin <= ?)
    )
    '''
    cursor.execute(query, (jour, heure_fin, heure_debut, heure_debut, heure_fin, heure_debut, heure_fin))
    return cursor.fetchone() is not None

#my version
def verifier_conflit(curseur, jour,session, annee, heure_debut, heure_fin):
    """
    Vérifie si un cours existe déjà dans l'intervalle de temps donné.

    :param jour: Jour du cours (e.g., 'lundi')
    :param heure_debut: Heure de début du cours (e.g., '10:00')
    :param heure_fin: Heure de fin du cours (e.g., '12:00')
    :param session: session durant laquelle on donne le cours
    :param annee: l'annee du cours
    :return: True si un conflit est détecté, False sinon
    """
    
    query = '''
    SELECT 1 FROM Horaire
    WHERE jour = ?
    AND session = ?
    AND annee = ?
    AND (
        (heure_debut <= ? AND heure_fin > ?)
        OR (heure_debut < ? AND heure_fin >= ?)
        OR (heure_debut >= ? AND heure_fin <= ?)
    )
    '''
    curseur.execute(query, (jour, session, annee, heure_fin, heure_debut, heure_debut, heure_fin, heure_debut, heure_fin))
    return cursor.fetchone() is not None

def ajouter_tache(nom, jour, heure_debut, heure_fin):
    """
    Ajoute une tâche après vérification des conflits.

    :param nom: Nom de la tâche
    :param jour: Jour de la tâche (e.g., 'lundi')
    :param heure_debut: Heure de début de la tâche (e.g., '10:00')
    :param heure_fin: Heure de fin de la tâche (e.g., '12:00')
    """
    if verifier_conflit(jour, heure_debut, heure_fin):
        print("Conflit détecté ! La tâche ne peut pas être enregistrée.")
    else:
        cursor.execute('''
        INSERT INTO taches (nom, jour, heure_debut, heure_fin)
        VALUES (?, ?, ?, ?)
        ''', (nom, jour, heure_debut, heure_fin))
        conn.commit()
        print("Tâche ajoutée avec succès.")

def afficher_taches():
    """
    Affiche toutes les tâches enregistrées.
    """
    cursor.execute('SELECT nom, jour, heure_debut, heure_fin FROM taches')
    taches = cursor.fetchall()
    if taches:
        for tache in taches:
            print(f"Tâche: {tache[0]}, Jour: {tache[1]}, Heure: {tache[2]} - {tache[3]}")
    else:
        print("Aucune tâche enregistrée.")
import os
from sys import platform

def clear_screen():
    """
    Efface l'écran de la console.
    """
    if platform.startswith('win'):  # Windows
        os.system('cls')
    elif platform.startswith('darwin') or platform.startswith('linux'):  # macOS / Linux
        os.system('clear')
    else:
        # Cas par défaut : tentative de clear pour d'autres systèmes
        os.system('cls' if os.name == 'nt' else 'clear')
    print("Écran nettoyé !")

def attendre_touche():
    """
    Attend que l'utilisateur appuie sur une touche pour continuer.
    """
    try:
        input("Appuyez sur une touche pour continuer...")
    except KeyboardInterrupt:
        pass  # Gère l'interruption par Ctrl+C


# Interface utilisateur simple
while True:
    
    print("\n1. Ajouter une tâche")
    print("2. Afficher les tâches")
    print("3. Quitter")

    choix = input("Choisissez une option: ")

    if choix == '1':
        clear_screen()
        nom = input("Nom de la tâche: ")
        jour = input("Jour (e.g., lundi): ").lower()
        heure_debut = input("Heure de début (HH:MM): ")
        heure_fin = input("Heure de fin (HH:MM): ")
        ajouter_tache(nom, jour, heure_debut, heure_fin)
        attendre_touche()
        clear_screen()
    elif choix == '2':
        afficher_taches()
        attendre_touche()
        clear_screen()
    elif choix == '3':
        break
    else:
        print("Option invalide, veuillez réessayer.")
        attendre_touche()
        clear_screen()

# Fermeture de la connexion à la base de données
conn.close()
