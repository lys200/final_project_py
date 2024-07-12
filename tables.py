import sqlite3
from time import sleep

def afficher_horaire(conn):
    """Fonction qui formatte l'affichage de tous les horaires 
    param conn: connection a la base de donnee
    """
    # Requête SQL pour obtenir les données nécessaires
    query = """
    SELECT H.annee, H.session, C.niveau, C.nom_fac, H.jour, H.heure_debut, H.heure_fin, H.nom_cours, H.code_salle
    FROM Horaire H
    JOIN Cours C ON H.code_cours = C.id_cours
    ORDER BY H.annee, H.session, C.niveau, C.nom_fac;
    """
    
    cursor = conn.execute(query)
    rows = cursor.fetchall()
        # Définition des jours de la semaine et des plages horaires

    jours = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi']
    heures = [f'{h:02}:00' for h in range(8, 17)]
    column_width = 15
    
    # Organisation des données par année, session, niveau, et faculté
    horaires = {}
    for row in rows:
        annee, session, niveau, faculte, jour, heure_debut, heure_fin, cours, salle = row
        key = (annee, session, niveau, faculte)
        
        if key not in horaires:
            horaires[key] = {heure: {jour: '' for jour in jours} for heure in heures}
        
        heure_debut_int = int(heure_debut.split(':')[0])
        heure_fin_int = int(heure_fin.split(':')[0])
        
        for heure in range(heure_debut_int, heure_fin_int + 1):
            heure_str = f'{heure:02}:00'
            if heure_str in horaires[key] and jour in horaires[key][heure_str]:
                if heure_fin_int - heure_debut_int > 2:
                    if heure == heure_debut_int:
                        horaires[key][heure_str][jour] = f"{"-"*15}"
                    elif heure == heure_fin_int:
                        horaires[key][heure_str][jour] = f"{"-"*15}"
                    elif heure == heure_debut_int + 1:
                        horaires[key][heure_str][jour] = f"{cours}"
                    elif heure == heure_debut_int + 2:
                        horaires[key][heure_str][jour] = f"{salle}"
                    else:
                        horaires[key][heure_str][jour] = '.' * (column_width - 1)
                
                elif heure_fin_int - heure_debut_int == 2:
                    if heure == heure_debut_int:
                        horaires[key][heure_str][jour] = f"{"-"*15}"
                    elif heure == heure_fin_int:
                        horaires[key][heure_str][jour] = f"{"-"*15}"
                    elif heure == heure_debut_int + 1:
                        horaires[key][heure_str][jour] = f"{cours} ({salle})"

                elif heure_fin_int - heure_debut_int < 2:
                    if heure == heure_debut_int:
                        horaires[key][heure_str][jour] = f"{"-"*15}"
                    elif heure == heure_fin_int:
                        horaires[key][heure_str][jour] = f"{cours} ({salle})"
    
    # Affichage de l'horaire
    for key, horaire in horaires.items():
        annee, session, niveau, faculte = key
        print(f"Horaire {session} {annee} - Niveau {niveau}, Faculté de {faculte}:")
        print(' ' * 15 + '+' + '+'.join('-' * (column_width + 2) for _ in jours) + '+' +'-'*17 + '+')
        # Affichage de l'en-tête
        entete = f"| {'Heure':<{column_width}} | " + ' | '.join(f"{jour.capitalize():<{column_width}}" for jour in jours) + " |"
        print(' ' * 15 + entete)
        print(' ' * 15 + '+' + '+'.join('-' * (column_width + 2) for _ in jours) + '+' +'-'*17 + '+')
        
        for heure in heures:
            row = f"| {heure:<{column_width}} | " + ' | '.join(f"{horaire[heure][jour]:<{column_width}}" for jour in jours) + " |"
            print(' ' * 15 + row)
        
        print(' ' * 15 + '+' + '+'.join('-' * (column_width + 2) for _ in jours) + '+' +'-'*17 + '+')
        print('\n' +' '*33 + '-'*91 + '\n')

# Exemple d'utilisation de la fonction
conn = sqlite3.connect('Gestion_des_salles.db')  # Remplacez 'database.db' par le chemin de votre base de données
afficher_horaire(conn)
conn.close()
