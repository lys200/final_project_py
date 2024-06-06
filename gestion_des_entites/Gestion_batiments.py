import Databases_pack.database as db
from gestion_des_contraintes.contraintes import is_empty
"""   base = 'test3.db'
    conn = db.connect_to_database(base)
    db.initialize_db(conn)
    #db.insert_data(conn,"Batiments", id_batiment="b", nombre_etages=4, salle_de_cours=18)
        #db.update_data(conn,"Batiments" ,'A', nombre_etages = 0, salle_de_cours=20)
    db.delete_Database(conn, 'Batiments', 'id_batiment', "b")
    bat = db.read_database(conn, "Batiments")
print(bat)
"""
class Gestion_Batiment:
    """Class contenant toutes les fonctions relative a la gestion des batiments"""
    #curseur = db.Connect_to_database("Gestion_des_salles.db")
    #db.initialize_db(curseur)
    #choix = 0
    def __init__(self, adm_id):
        self.curseur = db.connect_to_database("Gestion_des_salles.db")
        self.adm_id = adm_id
        db.initialize_conn(self.curseur)
        
    def enregistrer(self):
        """Enregistre un nouveau batiment"""
        while True:
            id_bat = input("Entrer le nom du batiment[A-D]: ")
            if id_bat in ['A', 'B', 'C', 'D']:
                break
            else: 
                print("Le batiment doit etre A, B, C ou D.\n")
        #verifier que le id_batiment n'exsite pas deja dans la table Batiment
        is_batiment = db.search_by_data(self.curseur, "batiments", "id_batiment", id_bat)
        #insertion des donnees dans la table batiments
        if is_batiment:
            print("Ce batiment est déja enregistré.")
        else:
            db.insert_data(self.curseur, "Batiments", id_batiment = id_bat, nombre_etages = 3, salle_de_cours = 18, salle_de_cours_disponibles = 18)
            print("Par défaut, le nombre d'étages est fixé à 3 et le nombre de salle par étage à 6.")
            print(f"Le Batiment {id_bat} est enregistré aves succès.\n")
            
    def lister(self):
        """Lister toutes les lignes de la table Batiments"""
        datas = db.read_database(self.curseur, "Batiments")
        if datas == []:
            print("Aucun batiment n'est encore enregistré.")
        else:
            print("Voici les informations enregistrées concernant les batiments:\n ")
            print("indexes|batiments|étages|salles|salles disponibles|")
            for data in datas:
                print(data[0], "\t|", data[1], "\t|", data[2],"\t|", data[3],"\t", data[4])

    def modifier(self):        
        """Modifie les infos d'un batiment"""
        name = is_empty("Entrer le nom/id du batiments a modifier:\n --> ")
        if db.verify_data(self.curseur, "Batiments", "id_batiment", name) == True:
            champs = input("Entrer le champs a modifier [id_Batiment]: ")
            if db.verify_column(self.curseur, "Batiments", champs) == True:
                new_data = is_empty(f"Entrer la nouvelle valeur du champ {champs},[A-B-C-D]:\n -->")
                if new_data :#in ['A','B','C','D']:
                    #db.update_data(self.curseur,"Batiments" ,'A', nombre_etages = 0, salle_de_cours=20)
                    print('champs=', champs)
                    print('new_data:', new_data)
                    db.update_data(self.curseur, "Batiments", name, id_batiment = new_data)
                    print('ligne55')
                else:
                    print("Id batiment invalide")
            else:
                print(f"la colonne {champs} n'ext pas dans la table Batiments.")
        else:
            print("Ce batiment n'est pas enregistré dans la base de données.")

    def rechercher(self):
        """Rechercher par filtre dans la table Batiments"""
        while True:
            print('\t','-'*8,"MENU RECHERCHER",'-'*8)
            print('\t','-'*32)
            print("Pour faire une recherche par filtre , vous devez choisir parmi les options suivantes")
            print("1- Rechercher par id_batiment")
            print("2- Rechercher par nombre de salle")
            print("3- Rechercher par Nombre d'étage")
            print("4- Retour au menu batiment.")
            choix = input("Faites votre choix: ")
            if choix == '1':
                id_batiment = is_empty("Entrer l'id du Batiment a afficher: \n --> ")
                if db.verify_data(self.curseur, "Batiments", "id_batiment", id_batiment) == True:
                    datas = db.search_by_data(self.curseur, "Batiments","id_batiment", id_batiment)
                    print("indexes|batiments|étages|salles| salles disponibles")
                    for data in datas:
                        print(data[0], "\t|", data[1], "\t|", data[2],"\t|", data[3],"\t|", data[4])
                else:
                    print("Ce batiment n'est pas enregistré dans la base de données.")
            elif choix == '2':
                nbre_salle = input("Entrer le nombre de salle: ")
                datas = db.search_by_data(self.curseur, "Batiments","salle_de_cours", nbre_salle)
                if datas == []:
                    print(f"Aucun batiment ne contient {nbre_salle} salle(s).")
                else:
                    print("indexes|batiments|étages|salles| salles disponibles")
                    for data in datas:
                        print(data[0], "\t|", data[1], "\t|", data[2],"\t|", data[3],"\t", data[4],"\n")
            elif choix == '3':
                nbre_etage = is_empty("Entrer le nombre de salle: \n -->")
                datas = db.search_by_data(self.curseur, "Batiments","nombre_etages", nbre_etage)
                if datas == []:
                    print(f"Aucun batiment ne contient {nbre_etage} étage(s).")
                else:
                    print("indexes|batiments|étages|salles| salles disponibles")
                    for data in datas:
                        print(data[0], "\t|", data[1], "\t|", data[2],"\t|", data[3],"\t", data[4],"\n")
            elif choix == '4':
                break

    def supprimer(self):
        id_batiment = is_empty("Entrer l'id du Batiment a supprimer:\n --> ")
        if db.verify_data(self.curseur, "Batiments", "id_batiment", id_batiment) == True:
            while True: 
                print(f"Etesvous sur de vouloir supprimer le batiment {id_batiment}?")
                choix = input("1- Supprimer 2- Annuler\n -->")
                if choix == '1':
                    db.delete_database(self.curseur, "Batiments", "id_batiment", id_batiment)
                    print("Suppression effectuée!")
                    break
                elif choix == '2':
                    break
                else:
                    print("Vous devez choisir entre l'option 1 et 2.")
        else:
            print("Ce batiment n'est pas enregistré dans la base de données.")
  
    def menu_batiment(self):
        """Fonction affichant les options de gestion des batiments"""
        while True:
            print('\t','-'*32)
            print('\t','-'*8,"MENU BATIMENT",'-'*8)
            print('\t','-'*32)
            print("Bienvenue au menu Batiments.")
            print("Veuillez choisir votre option.")
            if self.adm_id :
                print("1- Enregistrer un batiment.")
                print("2- Lister les batiments.")
                print("3- Rechercher les information d'un batiment.")
                print("4- Supprimer un batiment.")
                print("5- Retour au menu principal.")
                try:
                    choix = int(input("choix [1-5]: \n -->"))
                except Exception as e:
                    print("Erreur veuiller entrer un entier valide: ", e)
                else:
                    if choix < 1 or choix > 5:
                        print("Veuillez choisir un chiffre entre 1 et 5")
                    else:
                        if choix == 1:
                            self.enregistrer()
                        elif choix == 2:
                            self.lister()
                        elif choix == 3:
                            self.rechercher()
                        elif choix == 4:
                            self.supprimer()
                        elif choix == 5:
                            break   
            else:
                print("1- Enregistrer un batiment.")
                print("2- Lister les batiments.")
                print("3- Rechercher les information d'un batiment.")
                print("4- Supprimer un batiment.")
                print("5- Retour au menu principal.")
                try:
                    choix = int(input("choix [1-5]:\n -->"))
                except Exception as e:
                    print("Erreur veuiller entrer un entier valide: ", e)
                else:
                    if choix < 1 or choix > 5:
                        print("Entrée invalide. Veuillez choisir un chiffre entre 1 et 5.\n")
                    else:
                        if choix == 1:
                            print("Accès interdit. Seuls les admins peuvent faire des enregistrements.\n")
                        elif choix == 2:
                            self.lister()
                        elif choix == 3:
                            self.rechercher()
                        elif choix == 4:
                            print("Accès interdit. Seuls les admins peuvent faire des Suppressions.\n")
                        elif choix == 5:
                            break   

