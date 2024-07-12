# import sqlite3

# def afficher_donnees_table(database_path, table_name):
#     # Connexion a baz de done a
#     conn = sqlite3.connect(database_path)
#     cursor = conn.cursor()
    
#     # rekipere des noms de colonnes
#     cursor.execute(f"PRAGMA table_info({table_name})")
#     columns_info = cursor.fetchall()
#     column_names = [info[1] for info in columns_info]
    
#     # prendre les données de la table
#     cursor.execute(f"SELECT * FROM {table_name}")
#     rows = cursor.fetchall()
    
#     # Détermination de la largeur des colonnes
#     column_widths = [max(len(str(value)) for value in column) for column in zip(*([column_names] + rows))]
    
#     # Création d'une ligne de séparation
#     separator = '+' + '+'.join('-' * (width + 2) for width in column_widths) + '+'
    
#     # Affichage de l'entête de la table
#     header = '|' + '|'.join(f' {name:<{width}} ' for name, width in zip(column_names, column_widths)) + '|'
#     print(separator)
#     print(header)
#     print(separator)
    
#     # Affichage des lignes de la table
#     for row in rows:
#         line = '|' + '|'.join(f' {str(value):<{width}} ' for value, width in zip(row, column_widths)) + '|'
#         print(line)
#     print(separator)
    
#     # Fermeture de la connexion
#     cursor.close()
#     conn.close()

# # Exemple d'utilisation
# afficher_donnees_table('gestion_des_entites\Gestion_des_salles.db', 'Cours')


def afficher_entete(column_names):
    # Détermination de la largeur des colonnes
    column_widths = [len(name) for name in column_names]
    
    # Création d'une ligne de séparation
    separator = '+' + '+'.join('-' * (width + 2) for width in column_widths) + '+'
    
    # Affichage de l'entête de la table
    header = '|' + '|'.join(f' {name:<{width}} ' for name, width in zip(column_names, column_widths)) + '|'
    print(separator)
    print(header)
    print(separator)
    
    return column_widths, separator

def afficher_donnees(data, column_widths, separator):
    # Affichage des lignes de la table
    for row in data:
        line = '|' + '|'.join(f' {str(value):<{width}} ' for value, width in zip(row, column_widths)) + '|'
        print(line)
    print(separator)

# Exemple d'utilisation
entete = ['VoyageId', 'code_Personnel']
donnees = [
    [2, '001'],
    [1, '006'],
    [3, '009'],
    [4, '008'],
    [5, '001'],
    [6, '006'],
    [7, '001'],
    [8, '006'],
    [9, '001'],
    [10, '009']
]

# Affichage de l'entête et des données
column_widths, separator = afficher_entete(entete)
afficher_donnees(donnees, column_widths, separator)

def modifier(self):        
        """Modifie les infos d'un batiment"""
        name = is_empty("Entrer le nom/id du batiments a modifier (x pour quitter):").upper()
        if name == 'X':
            return
        elif db.verify_data(self.curseur, "Batiments", "id_batiment", name) == True:
            champs = is_empty("Entrer le champs a modifier [id_Batiment]: ")
            if db.verify_column(self.curseur, "Batiments", champs) == True:
                new_data = is_empty(f"Entrer la nouvelle valeur du champ {champs},[A-B-C-D]:")
                if new_data :
                    db.update_data(self.curseur, "Batiments", name, id_batiment = new_data)
                else:
                    print(' '*20,"Id batiment invalide")
            else:
                print(' '*20,f"la colonne {champs} n'ext pas dans la table Batiments.")
        else:
            print(' '*20,"Ce batiment n'est pas enregistré dans la base de données.")
