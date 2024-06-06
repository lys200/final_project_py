import Databases_pack.database as db
from gestion_des_contraintes.contraintes import is_empty
"""CREATE TABLE IF NOT EXISTS Salles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_salle TEXT, 
                num_salle INTEGER NOT NULL,
                id_batiment TEXT,
                etage INTEGER NOT NULL,
                nombre_de_siege INTEGER NOT NULL, 
                statut TEXT NOT NULL)
        """ 
class Gestion_Salle:
    """Class contenant toutes les fonctions relative a la gestion des Salles"""
    
    def __init__(self, adm_id):
        self.curseur = db.connect_to_database("Gestion_des_salles.db")
        self.adm_id = adm_id
        db.initialize_conn(self.curseur)
        
    def enregistrer(self):
        """Enregistre une nouvelle salle"""
        while True:
            numero_salle = is_empty("Entrer le numero de la salle[1-6]:\n --> ")
            if numero_salle in ['1', '2', '3', '4', '5','6']:
                break
            else: 
                print("Le numéro de la salle doit etre compris entre 1 et 6.\n")

        while True: 
            batiment = is_empty("Entrer le nom/id du batiment dans lequel se trouve la salle:\n --> ")
            #verifier que le id_batiment n'exsite pas deja dans la table Batiment
            is_batiment = db.search_by_data(self.curseur, "batiments", "id_batiment", batiment)
            #insertion des donnees dans la table batiments
            if is_batiment:
                while True:
                    num_etage = is_empty("Entrer le numéro d'étage dans lequel se trouve la salle:[0-2]\n --> ")
                    if int(num_etage) < 0 or int(num_etage) > (is_batiment[0][2]- 1):
                        print(f"Le numéro d'étage doit etre entre 0 pour le rez-de-chaussée et {is_batiment[0][2] -1}, pour le dernier étage.")
                    else:
                        break
                print(f"verification de l'existence de la salle {batiment}{num_etage}0{numero_salle}...")
                idsalle = f'{batiment}{num_etage}0{numero_salle}'
                print(idsalle)
                if db.verify_data(self.curseur,'Salles','id_salle', idsalle):
                    print("Cette salle a déeja été enregistrée dans la base de donnée.")
                    break
                else:
                    while True:
                        try:
                            sieges = int(is_empty("Entrer le nombre de sieges de la salle:\n --> "))
                        except Exception as e:
                            print("Entree invalide: ",e)
                        else:
                            if sieges < 0 or sieges > 70:
                                print("Le nombre de sieges doit logiquement etre compris entre 0 et 70 maximum.")
                            else:
                                db.insert_data(self.curseur, "Salles",num_salle= int(numero_salle), id_batiment = batiment, etage = int(num_etage), nombre_de_siege = sieges, statut = "Disponible" )
                                break
                    break
            else:
                print(f"Le Batiment {batiment} n'est pas enregistré dans la table Batiment.")
                print("Veuillez d'abord l'enregistrer dans le menu 'batiment' pour pouvoir enregistrer la salle.\n")
                ch = is_empty("1- Reessayer 2-Abandonner l'enregistrement\n -->")
                if ch == "1":
                    pass
                elif ch == '2':
                    break
                else:
                    print("Vous devez choisir entre 1 et 2.")


    def lister(self):
        """Lister toutes les salles de la table Salles"""
        datas = db.read_database(self.curseur, "Salles")
        if datas == []:
            print("\nAucune salle n'est encore enregistrée.\n")
        else:
            print("Voici les informations enregistrées concernant les Salles:\n ")
            print("indexes|Salles|num_salle|id_salle | etage | nombre de siege|statut |")
            for data in datas:
                print(data[0], "\t|", data[1], "\t|", data[2],"\t|", data[3],"\t", data[4], "\t", data[5],"\t", data[6])

    def modifier(self):        
        """Modifier les infos d'une salle"""
        id_salle = is_empty("Entrer le id de la salle a modifier: \n -->")
        if db.verify_data(self.curseur, "Salles", "id_salle", id_salle) :
                while True:
                    try:
                        sieges = int(is_empty("Entrer le nombre de sieges de la salle:\n --> "))
                    except Exception as e:
                        print("Entree invalide: ",e)
                    else:
                        if sieges < 0 or sieges > 70:
                            print("Le nombre de sieges doit logiquement etre compris entre 0 et 70 maximum.")
                        else:
                            db.update_data(self.curseur,"Salles", 'id_salle',id_salle, nombre_de_siege = sieges)
                            break
        else:
            print("Cette salle n'est pas enregistré dans la base de données.")

    def rechercher(self):
        """filtrer la table Salles"""
        while True:
            print('\t','-'*8,"MENU RECHERCHER SALLE",'-'*8)
            print('\t','-'*32)
            print("Pour faire une recherche par filtre , vous devez choisir entre les parmi options suivantes: ")
            print("1- Rechercher une salle par son id.")
            print("2- filtrer par numéro de salle.")
            print("3- Filtrer par étage.")
            print("4- Filtrer par batiment.")
            print("5- Filtrer par nombre de sièges.")
            print("6- Retour au menu Salle.")
            print("7- Quitter le programme. ")
            choix = is_empty("Faites votre choix: \n -->")
            
            if choix == '1':
                room_id = is_empty("Entrer l'id de la salle a afficher:\n --> ")
                if db.verify_data(self.curseur, "Salles", "id_salle", room_id) == True:
                    datas = db.search_by_data(self.curseur, "Salles","id_salle", room_id)
                    print("index|Salles|num_salle|id_salle | etage | nombre de siege|statut |")
                    for data in datas:
                        print(data[0], "\t|", data[1], "\t|", data[2],"\t|", data[3],"\t", data[4], "\t", data[5],"\t", data[6])
                else:
                    print("Cette salle n'est pas enregistrée dans la base de données.")

            elif choix == '2':
                numero_salle = is_empty("Entrer le numéro de salle:\n --> ")
                datas = db.search_by_data(self.curseur, "Salles","num_salle", numero_salle)
                if datas == []:
                    print(f"Aucun batiment ne contient {numero_salle} salle(s).")
                else:
                    print("indexes|Salles|num_salle|id_salle | etage | nombre de siege|statut |")
                    for data in datas:
                        print(data[0], "\t|", data[1], "\t|", data[2],"\t|", data[3],"\t", data[4], "\t", data[5],"\t", data[6])
            
            elif choix == '3':
                while True:
                    try:
                        num_etage = int(is_empty("Entrer l'étage:\n -->"))
                    except Exception as e:
                        print("L'entrée doit etre un entier: ", e)
                    else:
                        if num_etage< 0 or num_etage > 2:
                            print("Le numéro d'étage va de 0 a 2.")
                        else:
                            datas = db.search_by_data(self.curseur, "Salles","etage", num_etage )
                            if not datas:
                                 print(f"Aucune salle n'est enregistrée a l'étage {num_etage}")
                            else:
                                print("indexes|Salles|num_salle|id_salle | etage | nombre de siege|statut |")
                                for data in datas:
                                    print(data[0], "\t|", data[1], "\t|", data[2],"\t|", data[3],"\t", data[4], "\t", data[5],"\t", data[6])
                                break
            elif choix == '4':
                id_batiment = is_empty("Entrer l'id du batiment dont vous voulez afficher les salles:\n -->")
                if db.verify_data(self.curseur, "Salles","id_batiment", id_batiment):
                    datas = db.search_by_data(self.curseur, "Salles", "id_batiment", id_batiment)
                    print(f"Voici les informations des salles se trouvant au batiment {id_batiment}.\n")
                    print("_"*42)
                    print("indexes|Salles|num_salle|id_salle | etage | nombre de siege|statut |")
                    for data in datas:
                        print(data[0], "\t|", data[1], "\t|", data[2],"\t|", data[3],"\t", data[4], "\t", data[5],"\t", data[6])
    
            elif choix == '5':
                while True:
                    try:
                        sieges = int(is_empty("Entrer le nombre de siège[0 -70] :\n -->"))
                    except Exception as e:
                        print("L'entrée doit etre un entier: ", e)
                    else:
                        if sieges< 0 or sieges > 70:
                            print("Le nombre de sieges va de 0 a 70.")
                        else:
                            datas = db.search_by_data(self.curseur, "Salles","nombre_de_siege", sieges )
                            if not datas:
                                 print(f"Aucune salle ne contient {sieges} sièges")
                            else:
                                print(f"Voici la liste des salles contenant {sieges} sièges.")
                                print("indexes|Salles|num_salle|id_salle | etage | nombre de siege|statut |")
                                for data in datas:
                                    print(data[0], "\t|", data[1], "\t|", data[2],"\t|", data[3],"\t", data[4], "\t", data[5],"\t", data[6])
                                break
            elif choix == "6":
                break

            elif choix == '7':
                exit()
            else:
                print("Entrée invalide, Veuillez choisir entre les options proposées.")
    def supprimer(self):
        id_salle = is_empty("Entrer l'id de la salle a supprimer:\n --> ")
        if db.verify_data(self.curseur, "Salles", "id_salle", id_salle):
            while True: 
                print(f"Etes-vous sur de vouloir supprimer la salle {id_salle}?")
                choix = is_empty("1- Supprimer 2- Annuler\n -->")
                if choix == '1':
                    db.delete_database(self.curseur, "Salles", "id_salle", id_salle)
                    print(f"Suppression de la salle {id_salle} effectuée!")
                    break
                elif choix == '2':
                    break
                else:
                    print("Vous devez choisir entre les options 1 et 2.")
        else:
            print("Cette salle n'est pas enregistrée dans la base de données.")
  
    def menu_salle (self) :
        """Fonction affichant les options de gestion des Salles"""
        while True:
            print('\n\t','-'*32)        
            print('\t','-'*8,"MENU SALLE",'-'*8)
            print('\t','-'*32,'\n')        
            print("Bienvenue au menu Salles.")
            print("Veuillez choisir votre option.")
            print("1- Enregistrer une salle.")
            print("2- Lister les salles.")
            print("3- Rechercher une/des salle(s).")
            print("4- Modifier les informations d'une salle.")
            print("5- Supprimer une salle.")
            print("6- Retour au menu principal.")
            print("7- Quitter le programme.")
            try:
                choix = int(input("Veuillez choisir votre option.[1-7]: "))
            except Exception as e:
                print("Erreur veuiller entrer un entier valide: ", e)
            else:
                if choix < 1 or choix > 6:
                    print("Veuillez choisir un chiffre entre 1 et 7")
                else:
                    if self.adm_id :
                        if choix == 1:
                            self.enregistrer()
                        elif choix == 2:
                            self.lister()
                        elif choix == 3:
                            self.rechercher()
                        elif choix == 4:
                            self.modifier()
                        elif choix == 5:
                            self.supprimer()
                        elif choix == 6:
                            break  
                        else:
                            print("\n\tFermeture du programme...\n")
                            exit() 
                    else:
                        if choix == 1:
                            print("Accès interdit. Seuls les admins peuvent faire des enregistrements.\n")
                        elif choix == 2:
                            self.lister()
                        elif choix == 3:
                            self.rechercher()
                        elif choix == 4:
                            print("Accès interdit. Seuls les admins peuvent faire des modifications.\n")
                        elif choix == 5:
                            print("Accès interdit. Seuls les admins peuvent faire des suppressions.\n")
                        elif choix == 6:
                            break  
                        else:
                            print("\n\tFermeture du programme...\n")
                            exit()  

