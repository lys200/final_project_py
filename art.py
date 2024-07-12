import sqlite3


# Connexion à la base de données
conn = sqlite3.connect('database.db')  # Remplacez 'database.db' par le nom de votre base de données
cursor = conn.cursor()

# Requête SQL pour obtenir les données nécessaires
query = """
SELECT H.code_cours, H.nom_cours, H.code_salle, H.jour, H.heure_debut, H.heure_fin, H.session, H.annee, C.nom_fac, C.niveau
FROM Horaire H
JOIN Cours C ON H.code_cours = C.id_cours
WHERE H.session = 'Automne' AND H.annee = 2024 AND C.niveau = 2 AND C.nom_fac = 'Faculté de Medecine';
"""

cursor.execute(query)
results = cursor.fetchall()

# Fermeture de la connexion à la base de données
conn.close()

# Formatage de l'affichage
days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
hours = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]

# Initialisation du tableau
schedule = {day: {hour: "" for hour in hours} for day in days}

for row in results:
    code_cours, nom_cours, code_salle, jour, heure_debut, heure_fin, session, annee, nom_fac, niveau = row
    schedule[jour][heure_debut] = nom_cours

# Affichage du tableau
print("+---------+--------+--------+-----------+-------+")
print("| Heure   | Lundi  | Mardi  | Mercredi  | Jeudi | Vendredi | Samedi |")
print("+---------+--------+--------+-----------+-------+")
for hour in hours:
    row = [hour]
    for day in days:
        row.append(schedule[day][hour])
    print("| " + " | ".join(row) + " |")
print("+---------+--------+--------+-----------+-------+")
