import sqlite3

# Connexion à la base de données (ou création si elle n'existe pas)
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Création de la première table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Table1 (
    id INTEGER PRIMARY KEY,
    name TEXT
)
''')

# Création de la deuxième table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Table2 (
    id INTEGER PRIMARY KEY,
    table1_id INTEGER,
    value TEXT,
    FOREIGN KEY(table1_id) REFERENCES Table1(id)
)
''')

# Insertion de données dans la première table
cursor.execute("INSERT INTO Table1 (name) VALUES ('Alice')")
cursor.execute("INSERT INTO Table1 (name) VALUES ('Bob')")

# Insertion de données dans la deuxième table
cursor.execute("INSERT INTO Table2 (table1_id, value) VALUES (1, 'Value1')")
cursor.execute("INSERT INTO Table2 (table1_id, value) VALUES (2, 'Value2')")
cursor.execute("INSERT INTO Table2 (table1_id, value) VALUES (1, 'Value3')")

# Sauvegarde des modifications
conn.commit()

# Effectuer une jointure entre les deux tables
cursor.execute('''
SELECT Table1.name, Table2.value
FROM Table1
JOIN Table2 ON Table1.id = Table2.table1_id
''')

# Récupération et affichage des résultats
rows = cursor.fetchall()
for row in rows:
    print(row)

# Fermeture de la connexion
conn.close()

def faire_jointure(table1, table2, jointure_condition):
    try:
        # Connexion à la base de données (ou création si elle n'existe pas)
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()

        # Construction de la requête SQL pour la jointure
        query = f'''
        SELECT *
        FROM {table1}
        JOIN {table2} ON {jointure_condition}
        '''

        # Exécution de la requête
        cursor.execute(query)

        # Récupération des résultats de la jointure
        rows = cursor.fetchall()

        # Fermeture de la connexion
        conn.close()

        # Retourner les résultats
        return rows

    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        return None

# Exemple d'utilisation
resultat = faire_jointure("Table1", "Table2", "Table1.id = Table2.table1_id")
for row in resultat:
    print(row)
