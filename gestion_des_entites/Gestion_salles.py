import Databases_pack.database as db
from gestion_des_contraintes.contraintes import is_empty, banner,is_integer, afficher_donnees, afficher_entete,afficher_texte_progressivement, attendre_touche, clear_screen, afficher_texte_progressivement
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
        self.connection = db.connect_to_database("Gestion_des_salles.db")
        self.adm_id = adm_id
        db.initialize_conn(self.connection)
        
    def enregistrer(self):
        """Enregistre une nouvelle salle"""
        while True: 
            print(' '*20,"Entrer le nom/id du batiment dans lequel se trouve la salle:")
            batiment = is_empty("(x pour quitter)")
            if batiment == 'x':
                return
            #verifier que le id_batiment n'exsite pas deja dans la table Batiment
            is_batiment = db.search_by_data(self.connection, "batiments", "id_batiment", batiment.upper())
            #insertion des donnees dans la table batiments
            if is_batiment:
                while True:
                    print(' '*20,"Entrer le numéro d'étage dans lequel se trouve la salle:[1-3]")
                    num_etage = is_empty("(x pour quitter)").lower()
                    if num_etage == 'x':
                        return
                    elif is_integer(num_etage):
                        if int(num_etage) < 1 or int(num_etage) > 3:
                            print(f"Le numéro d'étage doit être entre 1 pour le rez-de-chaussée et 3 pour le dernier étage.")
                        else:
                            while True:
                                print(' '*20,f"voici les numeros de salle pour cette étage:")
                                numero_salles =  [f'{num_etage}01' ,f'{num_etage}02', f'{num_etage}03', f'{num_etage}04', f'{num_etage}05', f'{num_etage}06'] 
                                print(' '*20,f'{num_etage}01' ,f'\t{num_etage}02', f'\t{num_etage}03')
                                print(' '*20,f'{num_etage}04', f'\t{num_etage}05', f'\t{num_etage}06')
                                print(' '*20,"Choisir le numero de la salle[1-6]:")
                                numero_salle = is_empty("(x pour quitter)").lower()
                                if numero_salle == 'x':
                                    return
                                elif numero_salle in numero_salles:
                                    break
                                else: 
                                    print(' '*20,"Le numéro de la salle doit être dans la liste proposée.\n")
                            break
                    else:
                        print(' '*20,"L'entrée doit être un entier.")
                idsalle = f'{batiment.upper()}{numero_salle}'
                if db.verify_data(self.connection,'Salles','id_salle', idsalle):
                    print(' '*20,"Cette salle est deja enregistrée dans la base de donnée.")
                    attendre_touche()
                    break
                else:
                    while True:
                        try:
                            sieges = int(is_empty("Entrer le nombre de sieges de la salle:"))
                        except Exception as e:
                            print("L'entrée doit être un entier: ",e)
                        else:
                            if sieges < 0 or sieges > 70:
                                print(' '*20,"Le nombre de sieges doit logiquement etre compris entre 0 et 70 maximum.")
                            else:
                                db.insert_data(self.connection, "Salles",num_salle= int(numero_salle), id_batiment = batiment.upper(), etage = int(num_etage), nombre_de_siege = sieges)
                                # incrementer le nombre de salle du batiment
                                datas_batiment= db.search_by_data(self.connection, "Batiments", "id_batiment", batiment)
                                db.update_data(self.connection, "Batiments", "id_batiment", batiment.upper(), salle_de_cours = (datas_batiment[0][3] + 1))
                                attendre_touche()
                                break
                    break
            else:
                while True:
                    print(' '*20,f"Le Batiment {batiment} n'est pas enregistré dans la table Batiment.")
                    print(' '*20,"Veuillez d'abord l'enregistrer dans le menu 'batiment' pour pouvoir enregistrer la salle.\n")
                    ch = is_empty("1- Reessayer\t 2-Abandonner l'enregistrement")
                    if ch == "1":
                        break
                    elif ch == '2':
                        return
                    else:
                        print(' '*20,"Vous devez choisir entre 1 et 2.")
        
    def lister(self):
        """Lister toutes les salles de la table Salles"""
        datas = db.read_database(self.connection, "Salles")
        if datas:
            print(' '*20,"Voici les informations enregistrées concernant les Salles:\n ")
            columns = ['Index', 'Salles', 'numéro','batiment','étage', 'nombre de sièges']
            largeur, separateur = afficher_entete(columns)
            afficher_donnees(datas, largeur, separateur)
        else:
            print('\n', ' '*20,"Aucune salle n'est encore enregistrée.\n")
        attendre_touche()
   
    def modifier(self):        
        """Modifier les infos d'une salle"""
        print(' '*20,"Entrer le id de la salle a modifier:")       
        id_salle = is_empty("(x pour quitter):").upper()
        if id_salle == 'X':
            return

        elif db.verify_data(self.connection, "Salles", "id_salle", id_salle) :
                text = "\t\tPour éviter des conflits entre les données, "
                text2 = "\tvous avez seulement l'accès de modifier le nombre de sièges d'une salle. "
                afficher_texte_progressivement(text, 0.01)
                afficher_texte_progressivement(text2, 0.01)
                attendre_touche()
                while True:
                    try:
                        sieges = int(is_empty("Entrer le nombre de sieges de la salle:"))
                    except Exception as e:
                        print(' '*20,"Entree invalide: ",e)
                    else:
                        if sieges < 0 or sieges > 70:
                            print(' '*20,"Le nombre de sieges doit logiquement etre compris entre 0 et 70 maximum.")
                        else:
                            db.update_data(self.connection,"Salles", 'id_salle',id_salle, nombre_de_siege = sieges)
                            print(' '*20,"Modification réussie!")
                            break
        else:
            print(' '*20,"Cette salle n'est pas enregistré dans la base de données.")

    def rechercher(self):
        """filtrer la table Salles"""
        while True:
            print(' '*20,'\t','-'*8,"MENU RECHERCHER SALLE",'-'*8)
            print(' '*20,'\t','-'*32)
            print(' '*20,"Pour faire une recherche par filtre , vous devez choisir entre les parmi options suivantes: ")
            print(' '*20,"1- Rechercher une salle par son id.")
            print(' '*20,"2- filtrer par numéro de salle.")
            print(' '*20,"3- Filtrer par étage.")
            print(' '*20,"4- Filtrer par batiment.")
            print(' '*20,"5- Filtrer par nombre de sièges.")
            print(' '*20,"6- Retour au menu Salle.")
            print(' '*20,"7- Quitter le programme. ")
            choix = is_empty("Faites votre choix:")
            
            if choix == '1':
                print(' '*20,"Entrer l'id de la salle a afficher:")
                room_id = is_empty("(x pour quitter)").upper()
                if room_id == 'X':
                    return
                elif db.verify_data(self.connection, "Salles", "id_salle", room_id) == True:
                    print()
                    print(' '*20, f"Voici les informations la salles {room_id}.\n")
                    datas = db.search_by_data(self.connection, "Salles","id_salle", room_id)
                    columns = ['Index', 'Salles', 'numéro','batiment','étage', 'nombre de sièges']
                    largeur, separateur = afficher_entete(columns)
                    afficher_donnees(datas, largeur, separateur)
                else:
                    print(' '*20,"Cette salle n'est pas enregistrée dans la base de données.")
                attendre_touche()
                clear_screen()

            elif choix == '2':
                numero_salle = is_empty("Entrer le numéro de salle:")
                datas = db.search_by_data(self.connection, "Salles","num_salle", numero_salle)
                if datas:
                    columns = ['Index', 'Salles', 'numéro','batiment','étage', 'nombre de sièges']
                    largeur, separateur = afficher_entete(columns)
                    afficher_donnees(datas, largeur, separateur)
                else:
                    print(' '*20,f"Aucun batiment ne contient {numero_salle} salle(s).")
                attendre_touche()
                clear_screen()
            
            elif choix == '3':
                while True:
                    try:
                        num_etage = int(is_empty("Entrer l'étage:\n -->"))
                    except Exception as e:
                        print(' '*20,"L'entrée doit être un entier: ", e)
                    else:
                        if num_etage< 0 or num_etage > 2:
                            print(' '*20,"Le numéro d'étage va de 0 a 2.")
                        else:
                            datas = db.search_by_data(self.connection, "Salles","etage", num_etage )
                            if not datas:
                                 print(' '*20,f"Aucune salle n'est enregistrée a l'étage {num_etage}")
                            else:
                                columns = ['Index', 'Salles', 'numéro','batiment','étage', 'nombre de sièges']
                                largeur, separateur = afficher_entete(columns)
                                afficher_donnees(datas, largeur, separateur)
                                break
                attendre_touche()
                clear_screen()
            elif choix == '4':
                print(' '*20,"Entrer l'id du batiment dont vous voulez afficher les salles:")
                id_batiment = is_empty("(x pour quitter)").upper()
                if id_batiment == "X":
                    return
                elif db.verify_data(self.connection, "Salles","id_batiment", id_batiment):
                    datas = db.search_by_data(self.connection, "Batiment", "id_batiment", id_batiment)
                    if datas:
                        print(' '*20,f"Voici les informations des salles se trouvant au batiment {id_batiment}.\n")
                        columns = ['Index', 'Salles', 'numéro','batiment','étage', 'nombre de sièges']
                        largeur, separateur = afficher_entete(columns)
                        afficher_donnees(datas, largeur, separateur)
                        
                else:
                    print(' '*20,"Ce batiment n'est pas enregistré dans la base de donnée.")
                attendre_touche()
                clear_screen()
            elif choix == '5':
                while True:
                    try:
                        sieges = int(is_empty("Entrer le nombre de siège[0 -70]: "))
                    except Exception as e:
                        print(' '*20,"L'entrée doit être un entier: ", e)
                    else:
                        if sieges< 0 or sieges > 70:
                            print(' '*20,"Le nombre de sieges va de 0 a 70.")
                        else:
                            datas = db.search_by_data(self.connection, "Salles","nombre_de_siege", sieges )
                            if not datas:
                                 print(' '*20,f"Aucune salle ne contient {sieges} sièges")
                            else:
                                print(' '*20,f"Voici la liste des salles contenant {sieges} sièges.\n")
                                columns = ['Index', 'Salles', 'numéro','batiment','étage', 'nombre de sièges']
                                largeur, separateur = afficher_entete(columns)
                                afficher_donnees(datas, largeur, separateur)
                                break
                attendre_touche()
                clear_screen()
            elif choix == "6":
                break

            elif choix == '7':
                print(' '*20,"Fermeture du programme...")
                attendre_touche()
                exit()
            else:
                print(' '*20,"Entrée invalide, Veuillez choisir entre les options proposées.")

    def supprimer(self):
        print(' '*20,"Entrer l'id de la salle a supprimer:")
        id_salle = is_empty("(x pour quitter)").upper()
        if id_salle == 'X':
            return
        elif db.verify_data(self.connection, "Salles", "id_salle", id_salle):
            while True: 
                Warning_= f"\t\t\t\tATTENTION!\n"
                Warning_1 = f"La supression de la salle {id_salle} va entrainer la supression de toutes les horaires pour les cours qui y sont programmés.\n"
                print(Warning_)
                afficher_texte_progressivement(Warning_1, 0.01)
                print(' '*20,f"Etes-vous sur de vouloir supprimer la salle {id_salle}?")
                choix = is_empty("1- Supprimer 2- Annuler")
                if choix == '1':
                    db.delete_database(self.connection, "Salles", "id_salle", id_salle)
                    # decrementer le nombre de salle du batiment de la salle supprimee
                    datas_batiment= db.search_by_data(self.connection, "Batiments", "id_batiment", id_salle[0])
                    if datas_batiment:
                        db.update_data(self.connection, "Batiments", "id_batiment", id_salle[0], salle_de_cours = (datas_batiment[0][3] - 1))
                    
                    #recuperation des id des horaires de cette salle
                    horaires = db.search_by_data(self.connection, "Horaire", "code_salle", id_salle)
                    if horaires:
                        horaire_to_delete = []
                        for horaire in horaires:
                            horaire_to_delete.append(horaire[0])

                        for id_ in horaire_to_delete:
                            print(' '*20, f"supression de l'horaire {id_} de la base de données")
                            db.delete_database(self.connection, "Horaire", "id", id_)   
                    print(' '*20,f"Suppression de la salle {id_salle} effectuée!")
                    break
                elif choix == '2':
                    return
                else:
                    print(' '*20,"Vous devez choisir entre les options 1 et 2.")
        else:
            print(' '*20,"Cette salle n'est pas enregistrée dans la base de données.")
        attendre_touche()
  
    def menu_salle (self) :
        """Fonction affichant les options de gestion des Salles"""
        while True:
            clear_screen()
            banner()
            print(' '*20,'-'*32,'\n')        
            print(' '*20,'-'*8,"MENU SALLE",'-'*8)
            print(' '*20,'-'*32)        
            print(' '*20,"Bienvenue au menu Salles.\n")
            print(' '*20,"Veuillez choisir votre option.")
            print(' '*20,"1- Enregistrer une salle.")
            print(' '*20,"2- Lister les salles.")
            print(' '*20,"3- Rechercher une/des salle(s).")
            print(' '*20,"4- Modifier les informations d'une salle.")
            print(' '*20,"5- Supprimer une salle.")
            print(' '*20,"6- Retour au menu principal.")
            print(' '*20,"7- Quitter le programme.")
            try:
                choix = int(is_empty("Veuillez choisir votre option.[1-7]:"))
            except Exception as e:
                print("Erreur veuiller entrer un entier valide: ", e)
            else:
                if choix < 1 or choix > 7:
                    print(' '*20,"Veuillez choisir un chiffre entre 1 et 7")
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
                            print("\n",' '*20,"Fermeture du programme...\n")
                            attendre_touche()
                            exit() 
                    else:
                        if choix == 1:
                            print(' '*20,"Accès interdit. Seuls les admins peuvent faire des enregistrements.\n")
                        elif choix == 2:
                            self.lister()
                        elif choix == 3:
                            self.rechercher()
                        elif choix == 4:
                            print(' '*20,"Accès interdit. Seuls les admins peuvent faire des modifications.\n")
                        elif choix == 5:
                            print(' '*20,"Accès interdit. Seuls les admins peuvent faire des suppressions.\n")
                        elif choix == 6:
                            break  
                        else:
                            print("\n",' '*20,"Fermeture du programme...\n")
                            attendre_touche()
                            exit() 