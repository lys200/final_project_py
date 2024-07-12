
import sqlite3  # Importation du module sqlite3 pour interagir avec la base de données SQLite

def afficher_horaire(conn):
    # Requête SQL pour obtenir les données nécessaires
    query = """
    SELECT H.annee, H.session, C.niveau, C.nom_fac, H.jour, H.heure_debut, H.heure_fin, H.nom_cours, H.code_salle
    FROM Horaire H
    JOIN Cours C ON H.code_cours = C.id_cours
    ORDER BY H.annee, H.session, C.niveau, C.nom_fac;
    """
    
    # Exécution de la requête SQL
    cursor = conn.execute(query)
    rows = cursor.fetchall()
    
    # Définition des jours de la semaine et des plages horaires
    jours = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi']
    heures = [f'{h:02}:00' for h in range(8, 17)]
    column_width = 15  # Largeur des colonnes pour l'affichage
    
    # Organisation des données par année, session, niveau, et faculté
    horaires = {}
    for row in rows:
        annee, session, niveau, faculte, jour, heure_debut, heure_fin, cours, salle = row
        key = (annee, session, niveau, faculte)
        
        # Initialisation de la structure pour chaque clé unique
        if key not in horaires:
            horaires[key] = {heure: {jour: '' for jour in jours} for heure in heures}
        
        # Conversion des heures de début et de fin en entier pour faciliter la boucle
        heure_debut_int = int(heure_debut.split(':')[0])
        heure_fin_int = int(heure_fin.split(':')[0])
        
        # Remplissage de l'horaire pour chaque plage horaire couverte par le cours
        for heure in range(heure_debut_int, heure_fin_int + 1):
            heure_str = f'{heure:02}:00'
            if heure_str in horaires[key] and jour in horaires[key][heure_str]:
                if heure == heure_debut_int:
                    # Remplissage avec le nom du cours et le code de la salle
                    horaires[key][heure_str][jour] = f"{cours}\n{salle}"
                else:
                    # Remplissage des heures intermédiaires avec des points pour indiquer la continuité
                    horaires[key][heure_str][jour] = '.' * (column_width - 1)
    
    # Affichage de l'horaire
    for key, horaire in horaires.items():
        annee, session, niveau, faculte = key
        print(f"Horaire {session} {annee} - Niveau {niveau}, Faculté de {faculte}:")
        
        # Affichage de l'en-tête
        entete = f"| {'Heure':<{column_width}} | " + ' | '.join(f"{jour.capitalize():<{column_width}}" for jour in jours) + " |"
        print(' ' * 15 + entete)
        print(' ' * 15 + '+' + '+'.join('-' * (column_width + 2) for _ in jours) + '+')
        
        # Affichage de chaque ligne de l'horaire
        for heure in heures:
            row = f"| {heure:<{column_width}} | " + ' | '.join(f"{horaire[heure][jour]:<{column_width}}" for jour in jours) + " |"
            print(' ' * 15 + row)
        
        # Ligne de séparation après chaque tableau d'horaire
        print(' ' * 15 + '+' + '+'.join('-' * (column_width + 2) for _ in jours) + '+')
        print('\n' + '-'*80 + '\n')

# Exemple d'utilisation de la fonction
conn = sqlite3.connect('Gestion_des_salles.db')  # Connexion à la base de données SQLite
afficher_horaire(conn)  # Appel de la fonction pour afficher l'horaire
conn.close()  # Fermeture de la connexion à la base de données
