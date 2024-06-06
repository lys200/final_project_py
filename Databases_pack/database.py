"""
    Ce ficher contient les fonctions de gestion de la base de donnee
    pour la gestion des salles de cours au chcl.
"""
import sqlite3

def connect_to_database(conn_name):
    """connection a la database"""
    return sqlite3.connect(conn_name)
def initialize_conn(conn):
    """initialisation de la base de donnee"""
    try:
        curseur = conn.cursor()
         #creation des champ de la table "batiment"
        curseur.execute(
            """CREATE TABLE IF NOT EXISTS Batiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_batiment TEXT, 
                nombre_etages INTEGER,
                salle_de_cours INTEGER,
                salle_de_cours_disponibles INTEGER)
            """)

        #creation de la table Salle
        curseur.execute(
            """CREATE TABLE IF NOT EXISTS Salles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_salle TEXT, 
                num_salle INTEGER NOT NULL,
                id_batiment TEXT,
                etage INTEGER NOT NULL,
                nombre_de_siege INTEGER NOT NULL, 
                statut TEXT NOT NULL)
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
                SET id_salle = NEW.id_batiment || etage || "0" || num_salle
                where id = NEW.id;
            END;
        ''')

        #creation de la table cours
        curseur.execute(
            """CREATE TABLE IF NOT EXISTS Cours (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cours TEXT, 
                nom_cours TEXT NOT NULL,
                id_prof TEXT NOT NULL,
                nom_fac TEXT,
                duree REAL NOT NULL)
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
                SET id_cours = substr(NEW.nom_cours, 1, 3) || "_" || substr(NEW.nom_fac, 1, 3) || NEW.id
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
                SET id_cours = substr(NEW.nom_prof, 1, 3) || substr(NEW.prenom_prof, 1, 3) || NEW.id
                WHERE id = NEW.id;
            END;
        ''')
        #creation de la table horaires
        curseur.execute(
            """CREATE TABLE IF NOT EXISTS Horaire (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code_cours TEXT NOT NULL,
                code_salle TEXT NOT NULL,
                jour TEXT NOT NULL,
                session INTEGER NOT NULL,
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
        print("Insertion réussie!!!")

#cette fonction prend en param la table en question et la base de donnee
#puis retourne les donnees de la table en question
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

def update_data(conn, table_name,  id_entite, **kwargs):
    """Fonction pour modifier les donnees d'une table"""
    #prend en parametres: la conn, le nom de la table, le nom de la cle primaire, 
    #la valeur de l'id a modifier ainsi que l'ensenbles des colonnes a modifier , 
    curseur = conn.cursor()
    # Préparer les colonnes et les valeurs pour la mise à jour
    columns = ', '.join(f'{key} = ?' for key in kwargs)
    print("cols =", columns)
    #values = tuple(kwargs.values())
    values = tuple(kwargs.values()) + (id_entite,)
    print("vas =", values)
    # Préparer la requête de mise à jour
    query = f'UPDATE {table_name} SET {columns} WHERE id_batiment = ?'
    print("query=", query)
    # Exécuter la requête avec les valeurs fournies
    curseur.execute(query, values)
    conn.commit()
    print("Modification effectuée!\n")

def delete_database(conn, table_name, id_name, id_value):
    """fonction pour supprimmer n'inporte quelle info de n'inporte quelle table"""
    #prend en parametres: la conn, le nom de la table, le nom de la cle primaire, 
    #la valeur de l'id a supprimer
    curseur = conn.cursor()
    query = f"DELETE FROM {table_name} WHERE {id_name} = ?"
    curseur.execute(query,  id_value)
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
