import sqlite3

# Connexion à la base de données SQLite
conn = sqlite3.connect('university.db')
cursor = conn.cursor()

# Création des tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS cours (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    faculte TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS horaire (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cours_id INTEGER,
    jour TEXT NOT NULL,
    heure TEXT NOT NULL,
    FOREIGN KEY (cours_id) REFERENCES cours(id)
)
''')

# Fonction pour insérer un cours
def inserer_cours():
    nom = input("Entrez le nom du cours: ")
    faculte = input("Entrez la filière du cours: ")
    cursor.execute('''
    INSERT INTO cours (nom, faculte) VALUES (?, ?)
    ''', (nom, faculte))
    conn.commit()

# Fonction pour insérer un horaire
def inserer_horaire():
    cours_id = input("Entrez l'ID du cours: ")
    jour = input("Entrez le jour de l'horaire: ")
    heure = input("Entrez l'heure de l'horaire: ")
    cursor.execute('''
    INSERT INTO horaire (cours_id, jour, heure) VALUES (?, ?, ?)
    ''', (cours_id, jour, heure))
    conn.commit()

# Fonction pour afficher les horaires des cours en Informatique
def afficher_horaires_informatique():
    cursor.execute('''
    SELECT cours.nom, horaire.jour, horaire.heure
    FROM cours
    JOIN horaire ON cours.id = horaire.cours_id
    WHERE cours.faculte = 'Informatique'
    ''')
    rows = cursor.fetchall()
    for row in rows:
        print(f"Cours: {row[0]}, Jour: {row[1]}, Heure: {row[2]}")

# Menu utilisateur
while True:
    print("\n1. Ajouter un cours")
    print("\n2. Ajouter un horaire")
    print("\n3. Afficher les horaires des cours en Informatique")
    print("\n4. Quitter")
    
    choix = input("\nEntrez votre choix: ")
    
    if choix == '1':
        inserer_cours()
    elif choix == '2':
        inserer_horaire()
    elif choix == '3':
        afficher_horaires_informatique()
    elif choix == '4':
        break
    else:
        print("Choix invalide. Veuillez réessayer.")

# Fermeture de la connexion
conn.close()
