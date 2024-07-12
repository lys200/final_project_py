"""
    Ce ficher contient les fonctions de gestion de la base de donnees
    pour la gestion des salles de cours au chcl.
"""
import sqlite3

def connect_to_database(db_name):
    """connection a la database"""
    return sqlite3.connect(db_name)

def initialize_conn(conn):
    """initialisation de la base de donnees"""
    try:
        curseur = conn.cursor()
         #creation des champ de la table "batiment"
        curseur.execute(
            """CREATE TABLE IF NOT EXISTS Batiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_batiment TEXT, 
                nombre_etages INTEGER,
                salle_de_cours INTEGER
                )
            """)

        #creation de la table Salle
        curseur.execute(
            """CREATE TABLE IF NOT EXISTS Salles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_salle TEXT, 
                num_salle INTEGER NOT NULL,
                id_batiment TEXT,
                etage INTEGER NOT NULL,
                nombre_de_siege INTEGER NOT NULL
                )
        """ )

        #creation de declencheurs pour generer les id composés
        #supprimer le declencheur s'il existe deja
        curseur.execute('''
            DROP TRIGGER IF EXISTS after_insert_salles
        ''')
        #creer du declencheur
        curseur.execute('''
            CREATE TRIGGER after_insert_salles
            AFTER INSERT ON Salles
            FOR EACH ROW
            BEGIN
                UPDATE Salles
                SET id_salle = NEW.id_batiment || num_salle
                where id = NEW.id;
            END;
        ''')
        #creation de la table cours
        curseur.execute(
            """CREATE TABLE IF NOT EXISTS Cours (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cours TEXT, 
                nom_cours TEXT,
                nom_fac TEXT,
                niveau INTEGER NOT NULL,
                id_prof TEXT NOT NULL,
                duree TEXT NOT NULL)
        """)

        #creation du declencheur pour la table cours
        curseur.execute('''
            DROP TRIGGER IF EXISTS after_insert_cours
        ''')
        curseur.execute('''
            CREATE TRIGGER after_insert_cours
            AFTER INSERT ON Cours
            FOR EACH ROW
            BEGIN
                UPDATE Cours
                SET id_cours = substr(NEW.nom_cours, 1, 3) || "_" || substr(NEW.nom_fac, 1, 3)|| "_" ||'L'|| NEW.niveau
                WHERE id = NEW.id;
            END; ''')
        #creation de la table professeurs
        curseur.execute(
            """CREATE TABLE IF NOT EXISTS Professeurs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_prof TEXT PRYMARY KEY, 
                nom_prof TEXT NOT NULL,
                prenom_prof TEXT NOT NULL,
                tel_prof TEXT NOT NULL,
                email TEXT NOT NULL)
        """)

        #creation du declencheur pour la table Professeurs
        curseur.execute('''
            DROP TRIGGER IF EXISTS after_insert_prof
        ''')
        curseur.execute('''
            CREATE TRIGGER after_insert_prof
            AFTER INSERT ON Professeurs
            FOR EACH ROW
            BEGIN
                UPDATE Professeurs
                SET id_prof = substr(NEW.nom_prof, 1, 3) || substr(NEW.prenom_prof, 1, 3) || NEW.id
                WHERE id = NEW.id;
            END;
        ''')
        #declencheur pour mettre a jour l'id apres modification de la table professeurs
        curseur.execute('''
            DROP TRIGGER IF EXISTS after_update_prof
        ''')
        curseur.execute('''
            CREATE TRIGGER after_update_prof
            AFTER UPDATE ON Professeurs
            FOR EACH ROW
            BEGIN
                UPDATE Professeurs
                SET id_prof = substr(NEW.nom_prof, 1, 3) || substr(NEW.prenom_prof, 1, 3) || NEW.id
                WHERE id = NEW.id;
            END;
        ''')
        #creation de la table horaires
        curseur.execute(
            """CREATE TABLE IF NOT EXISTS Horaire (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code_cours TEXT NOT NULL,
                nom_cours TEXT NOT NULL,
                code_salle TEXT NOT NULL,
                jour TEXT NOT NULL,
                heure_debut TEXT NOT NULL,
                heure_fin TEXT NOT NULL,
                session TEXT NOT NULL,
                annee INTEGER NOT NULL)
        """)
        #creation de la table des administrateurs
        curseur.execute(
            """CREATE TABLE IF NOT EXISTS Administrateurs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                id_admin TEXT, 
                nom_admin TEXT NOT NULL,
                prenom_admin TEXT NOT NULL,
                password TEXT NOT NULL)
        """)
        #creation du declencheur pour la table des administrateurs
        curseur.execute('''DROP TRIGGER IF EXISTS after_insert_admin''')
        curseur.execute('''
            CREATE TRIGGER after_insert_admin
            AFTER INSERT ON Administrateurs
            FOR EACH ROW
            BEGIN
                UPDATE Administrateurs
                SET id_admin = "admin_" || substr(NEW.nom_admin, 1, 3) || substr(NEW.prenom_admin, 1, 3) || NEW.id
                WHERE id = NEW.id;
            END;
        ''')
        curseur.close()
    except sqlite3.OperationalError as e:
        print("Erreur d'initialisation de la base de donnee: ", e)

#------------------------fonctions de gestion des donnees dans les tables-------------------------
def insert_data(conn, table_name, **kwargs):
    """fonction pour inserer les donnees dans les tables"""
    #en parametres: la base de donnee, le nom de la table, les donnees a inserer
    try:
        curseur = conn.cursor()
        # Préparer les colonnes et les valeurs pour l'insertion
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join('?' for _ in kwargs)
        values = tuple(kwargs.values())
        # Préparer la requête d'insertion
        query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
        # Exécuter la requête avec les valeurs fournies
        curseur.execute(query, values)
        conn.commit()
    except sqlite3.OperationalError as error:
        print(f"Echec de l'insertion des donnees dans la table {table_name}", error)
    except sqlite3.IntegrityError as e:
        print(f"Erreur d'integrite dans la table {table_name}:", e)
        #print("veuillez verifier que cette id se trouve deja dans la table , puis reesayer ")
    else:
        print('\n',' '*20,"Insertion réussie!!!")

def read_database(conn, table_name):
    """fonction de lecture des tables de la base de donnees"""
    try:
        curseur = conn.cursor()
        query = f'SELECT * FROM {table_name}'
        curseur.execute(query)
        datas = curseur.fetchall()
        return  datas
    except sqlite3.OperationalError as e:
        print('erreur: ', e)

def search_by_data(conn, table_name, column_name, search_value):
    """Fonction pour rechercher une valeur dans la table/filtrer"""
    cursor = conn.cursor()
    # Préparer la requête de recherche
    query = f"SELECT * FROM {table_name} WHERE {column_name} LIKE ?"
    # Exécuter la requête avec la valeur de recherche
    cursor.execute(query, (f"%{search_value}%",))
    # Récupérer tous les résultats
    rows = cursor.fetchall()
    return rows

def update_data(conn, table_name,  id_entite, id_value,**kwargs):
    """Fonction pour modifier les donnees d'une table"""
    # prend en parametres: la conn, le nom de la table, le nom de la cle primaire,
    # la valeur de l'id a modifier ainsi que l'ensenbles des colonnes a modifier,
    curseur = conn.cursor()
    # Préparer les colonnes et les valeurs pour la mise à jour
    columns = ', '.join(f'{key} = ?' for key in kwargs)
    values = tuple(kwargs.values()) + (id_value,)
    # Préparer la requête de mise à jour
    query = f'UPDATE {table_name} SET {columns} WHERE {id_entite} = ?'
    # Exécuter la requête avec les valeurs fournies
    curseur.execute(query, values)
    conn.commit()

def delete_database(conn, table_name, id_name, id_value):
    """fonction pour supprimmer n'inporte quelle info de n'inporte quelle table"""
    #prend en parametres: la conn, le nom de la table, le nom de la cle primaire,
    #la valeur de l'id a supprimer
    curseur = conn.cursor()
    query = f"DELETE FROM {table_name} WHERE {id_name} = ?"
    curseur.execute(query,  (id_value,))
    conn.commit()

def verify_data(conn, table_name, column_name, valeur):
    """
    Vérifie si une information est deja enregistree dans la table ou l'on veut faire l'insertion.
    -return: True si la valeur existe, False sinon
    """
    try:
        curseur = conn.cursor()
        query = f"SELECT 1 FROM {table_name} WHERE {column_name} = ? LIMIT 1"
        curseur.execute(query, (valeur,))
        result = curseur.fetchone()
        #curseur.close()
        #conn.close()
        return result is not None
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        return False

def verify_column(conn, table_name, column_name):
    """
    Vérifie si une colonne existe dans une table SQLite3.
    :param db_path: Chemin vers la base de données SQLite3
    :param table_name: Nom de la table
    :param column_name: Nom de la colonne à vérifier
    :return: True si la colonne existe, False sinon
    """
    try:
        # Connexion à la base de données
        cursor = conn.cursor()
        # Exécution de la requête PRAGMA pour obtenir les informations des colonnes
        query = f"PRAGMA table_info({table_name})"
        cursor.execute(query)
        columns_info = cursor.fetchall()
        # Vérification de l'existence de la colonne
        for column in columns_info:
            if column[1] == column_name:
                return True
        return False
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        return False

def filter_table(conn, table_name, **args):
    """
    Permet d'afficher autant de filtres possibles pour une table en utilisant des arguments nommés.
    """

    """
    :param cursor: Le curseur de la base de données.
    :param table_name: Le nom de la table dans laquelle effectuer la recherche.
    :param args: Les paires colonne=valeur pour filtrer les résultats.
    :return: Les résultats de la requête filtrée.
    """
    curseur = conn.cursor()
    if not args:
        query = f"SELECT * FROM {table_name}"
        curseur.execute(query)
        return curseur.fetchall()
    where_clause = " AND ".join([f"{col} = ?" for col in args.keys()])
    query = f"SELECT * FROM {table_name} WHERE {where_clause}"
    curseur.execute(query, tuple(args.values()))
    datas = curseur.fetchall()
    return datas

def verifier_conflit(conn, jour,session, annee, heure_debut, heure_fin, salle):
    """
    Vérifie si un cours existe déjà dans l'intervalle de temps donné.
    """
    """
    :param salle: salle ou devrait se derouler le cours (e.g., 'C204')
    :param jour: Jour du cours (e.g., 'lundi')
    :param heure_debut: Heure de début du cours (e.g., '10:00')
    :param heure_fin: Heure de fin du cours (e.g., '12:00')
    :param session: session durant laquelle on donne le cours
    :param annee: l'annee du cours
    :return: True si un conflit est détecté, False sinon
    """
    curseur = conn.cursor()
    #si un cours se deroule dans cette salle , durant cette meme session de la meme annee
    # dans l'intervalle des heures qui coincident , il y a conflit
    # e.g: bio en C203 session 2 anneee 2023 a 12h-13h et physique en c203 session 2 annee 2023 a 12h-13h
    query = '''
    SELECT 1 FROM Horaire
    WHERE code_salle = ?
    AND jour = ?
    AND session = ?
    AND annee = ?
    AND (
        (heure_debut <= ? AND heure_fin > ?)
        OR (heure_debut < ? AND heure_fin >= ?)
        OR (heure_debut >= ? AND heure_fin <= ?)
    )
    '''
    curseur.execute(query,
                    (salle, jour, session, annee, heure_fin, heure_debut, heure_debut, heure_fin, heure_debut, heure_fin))
    return curseur.fetchone() is not None

def faire_jointure(conn, table1, table2, colonne_table1, colonne_table2, colonne_afficher1, colonne_afficher2, condition):
    """"fait jointure entre les tables"""
    try:
        cursor = conn.cursor()
        query = f'''
        SELECT {colonne_afficher1}
        FROM {table1}
        JOIN {table2} ON {table1}.{colonne_table1} = {table2}.{colonne_table2}
        WHERE {condition}
        '''
        print(query)
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erreur: {e}")
        return None
def get_column_values_starting_with(conn, table, column, starting_letter):
    """verifie  si les colonnes commencent par telle ou telle lettre """
    try:
        cursor = conn.cursor()
        query = f'''
                    SELECT {column}
                    FROM {table}
                    WHERE {column} LIKE ?
        '''
        cursor.execute(query, (f'{starting_letter}%',))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
   
def afficher_horaires(conn, faculte=None, niveau=None, id_prof=None):
    """Fonction affichant les horaires"""
    # Connexion à la base de données
    cursor = conn.cursor()
    # Construire la requête SQL
    query = f"""
    SELECT Horaire.*
    FROM Horaire
    JOIN Cours ON Horaire.code_cours = Cours.id_cours
    WHERE 1=1
    """
    # Ajouter les conditions en fonction des paramètres donnés
    params = []
    if faculte:
        query += " AND Cours.nom_fac = ?"
        params.append(faculte)
    if niveau:
        query += " AND Cours.niveau = ?"
        params.append(niveau)
    if id_prof:
        query += " AND Cours.id_prof = ?"
        params.append(id_prof)
    # Exécuter la requête et récupérer les résultats
    cursor.execute(query, params)
    return cursor.fetchall()

def afficher_horaire(conn):
    """Extraction des données"""
    cursor = conn.execute("SELECT * FROM horaire ORDER BY annee, session, niveau, faculte")
    rows = cursor.fetchall()
    jours = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi']
    heures = [f'{h:02}:00' for h in range(8, 17)]
    column_width = 15
    # Organisation des données par année, session, niveau, et faculté
    horaires = {}
    for row in rows:
        annee, session, niveau, faculte, jour, heure_debut, heure_fin, \
            cours = row[5], row[6], row[7], row[8], row[1], row[2], row[3], row[4]
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
                    # afficher_entete(['Heure'] + [jour.capitalize() for jour in jours], column_width)
                    for heure in heures:
                        row = f"| {heure:<{column_width}} | " + ' | '.\
                            join(f"{horaire[heure][jour]:<{column_width}}" for jour in jours) + " |"
                        print(' ' * 15 + row)
                    print(' ' * 15 + '+' + '+'.join('-' * (column_width + 2) for _ in jours) + '+')
                    print('\n' + '-'*80 + '\n')
