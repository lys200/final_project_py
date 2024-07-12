import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('database.db')

# Fonction pour créer la table et insérer des données pour les tests
def create_and_insert_data():
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS horaire (
                id INTEGER PRIMARY KEY,
                jour TEXT,
                heure_debut TEXT,
                heure_fin TEXT,
                cours TEXT,
                annee TEXT,
                session TEXT,
                niveau TEXT,
                faculte TEXT
            )
        ''')
        conn.execute('DELETE FROM horaire')
        data = [
            ('lundi', '10:00', '12:00', 'Maths', '2024', 'Automne', '1', 'Medecine'),
            ('mardi', '09:00', '11:00', 'Physique', '2024', 'Automne', '1', 'Medecine'),
            ('mercredi', '08:00', '09:00', 'Chimie', '2024', 'Automne', '1', 'Medecine'),
            ('jeudi', '14:00', '16:00', 'Informatique', '2024', 'Automne', '1', 'Medecine'),
            ('vendredi', '10:00', '11:00', 'Anglais', '2024', 'Automne', '1', 'Medecine'),
            ('lundi', '10:00', '12:00', 'Maths', '2023', 'Printemps', '1', 'Medecine'),
            ('mardi', '09:00', '11:00', 'Physique', '2023', 'Printemps', '1', 'Medecine'),
            ('mercredi', '10:00', '12:00', 'Biologie', '2024', 'Automne', '2', 'Medecine'),
            ('jeudi', '08:00', '10:00', 'Philosophie', '2024', 'Automne', '2', 'Medecine')
        ]
        conn.executemany('INSERT INTO horaire (jour, heure_debut, heure_fin, cours, annee, session, niveau, faculte) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', data)

# Fonction pour afficher l'entête formatée
def afficher_entete(column_names, column_width):
    separateur = '+' + '+'.join('-' * (column_width + 2) for _ in column_names) + '+'
    header = '|' + '|'.join(f' {name:<{column_width}} ' for name in column_names) + '|'
    print(' ' * 15 + separateur)
    print(' ' * 15 + header)
    print(' ' * 15 + separateur)

# Fonction pour afficher l'horaire
def afficher_horaire():
    # Extraction des données
    cursor = conn.execute("SELECT * FROM horaire ORDER BY annee, session, niveau, faculte")
    rows = cursor.fetchall()
    
    jours = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi']
    heures = [f'{h:02}:00' for h in range(8, 17)]
    column_width = 15
    
    # Organisation des données par année, session, niveau, et faculté
    horaires = {}
    for row in rows:
        annee, session, niveau, faculte, jour, heure_debut, heure_fin, cours = row[5], row[6], row[7], row[8], row[1], row[2], row[3], row[4]
        
        if annee not in horaires:
            horaires[annee] = {}
        if session not in horaires[annee]:
            horaires[annee][session] = {}
        if niveau not in horaires[annee][session]:
            horaires[annee][session][niveau] = {}
        if faculte not in horaires[annee][session][niveau]:
            horaires[annee][session][niveau][faculte] = {heure: {jour: '' for jour in jours} for heure in heures}
        
        heure_debut_int = int(heure_debut.split(':')[0])
        heure_fin_int = int(heure_fin.split(':')[0])
        
        for heure in range(heure_debut_int, heure_fin_int + 1):
            heure_str = f'{heure:02}:00'
            if heure_str in horaires[annee][session][niveau][faculte] and jour in horaires[annee][session][niveau][faculte][heure_str]:
                if heure == heure_debut_int:
                    horaires[annee][session][niveau][faculte][heure_str][jour] = cours
                else:
                    horaires[annee][session][niveau][faculte][heure_str][jour] = '.' * (column_width - 1)
    
    # Affichage de l'horaire
    for annee, sessions in horaires.items():
        for session, niveaux in sessions.items():
            for niveau, facultes in niveaux.items():
                for faculte, horaire in facultes.items():
                    print(f"Horaire {session} {annee} - Niveau {niveau}, Faculté de {faculte}:")
                    afficher_entete(['Heure'] + [jour.capitalize() for jour in jours], column_width)
                    for heure in heures:
                        row = f"| {heure:<{column_width}} | " + ' | '.join(f"{horaire[heure][jour]:<{column_width}}" for jour in jours) + " |"
                        print(' ' * 15 + row)
                    print(' ' * 15 + '+' + '+'.join('-' * (column_width + 2) for _ in jours) + '+')
                    print('\n' + '-'*80 + '\n')

# Création de la table et insertion des données pour les tests
create_and_insert_data()
# Affichage de l'horaire
afficher_horaire()
