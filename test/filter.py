def filter_table(cursor, table_name, **args):
    """
    Permet d'afficher autant de filtres possibles pour une table en utilisant des arguments nommés.

    :param cursor: Le curseur de la base de données.
    :param table_name: Le nom de la table dans laquelle effectuer la recherche.
    :param args: Les paires colonne=valeur pour filtrer les résultats.
    :return: Les résultats de la requête filtrée.
    """
    if not args:
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        return cursor.fetchall()

    where_clause = " AND ".join([f"{col} = ?" for col in args.keys()])
    query = f"SELECT * FROM {table_name} WHERE {where_clause}"
    cursor.execute(query, tuple(args.values()))
    return cursor.fetchall()

# Exemple d'utilisation
import sqlite3

# Connexion à la base de données (remplacez 'ma_base_de_donnees.db' par votre propre fichier de base de données)
conn = sqlite3.connect('ma_base_de_donnees.db')
cursor = conn.cursor()

# Création d'un exemple de table 'Personnel' pour la démonstration
cursor.execute('''
CREATE TABLE IF NOT EXISTS Personnel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    age INTEGER,
    taille REAL,
    cheveu TEXT
)
''')

# Insertion de quelques données pour la démonstration
'''cursor.execute("INSERT INTO Personnel (age, taille, cheveu) VALUES (26, 1.6, 'crepus')")
cursor.execute("INSERT INTO Personnel (age, taille, cheveu) VALUES (30, 1.8, 'lisse')")
cursor.execute("INSERT INTO Personnel (age, taille, cheveu) VALUES (26, 1.6, 'crepus')")
cursor.execute("INSERT INTO Personnel (age, taille, cheveu) VALUES (30, 1.8, 'boucle')")
cursor.execute("INSERT INTO Personnel (age, taille, cheveu) VALUES (26, 1.6, 'lisse')")
cursor.execute("INSERT INTO Personnel (age, taille, cheveu) VALUES (30, 1.8, 'lisse')")
conn.commit()'''

# Utilisation de la fonction pour trouver les personnes avec âge 26, taille 1.6m, cheveu crépus
resultats = filter_table(cursor, 'Personnel', age=30, taille=1.8)

# Affichage des résultats
for row in resultats:
    print(row)

# Fermeture de la connexion
conn.close()
