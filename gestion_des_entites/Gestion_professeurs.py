import Databases_pack.database as db
from gestion_des_contraintes.contraintes import is_empty, is_valid_email, is_valid_phone_number, display_list_columns
'''id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_prof TEXT PRYMARY KEY, 
                nom_prof TEXT NOT NULL,
                prenom_prof TEXT NOT NULL,
                tel_prof TEXT NOT NULL,
                email TEXT NOT NULL'''

class Gestion_Professeur:
    """Class contenant toutes les fonctions relative a la gestion des Salles"""
    
    def __init__(self, adm_id):
        self.curseur = db.connect_to_database("Gestion_des_salles.db")
        self.adm_id = adm_id
        db.initialize_conn(self.curseur)
        
    def enregistrer(self):
        """Enregistre un nouveau professeur"""
        nom = is_empty("Entrer le nom du professeur: (x pour quitter)\n -->")
        if nom == 'x':
            return   
        prenom = is_empty("Entrer le prenom du professeur: (x pour quitter)\n -->")
        if prenom == 'x':
            return
        while True:
            email = is_empty("Entrer l'email du prof: \n -->")
            if email == 'x':
                return
            elif is_valid_email(email):
                break
            else:
                print("Email invalide.\nExemple: something@domain.com")
        while True:
            tel = is_empty("Entrer le telephone du prof: (x pour quitter)\n -->")
            if tel == 'x':
                return
            elif is_valid_phone_number(tel):
                db.insert_data(self.curseur, "Professeurs", nom_prof = nom, prenom_prof = prenom, tel_prof = tel, email = email)
                print(f"Le professeur {nom} {prenom} est enregistré avec succès.")
                break
            else:
                print("Telephone invalide. Exemple de formats valide:")
                print("(123) 456-7890")  # True
                print("123-456-7890")    # True
                print("123 456 7890")   # True
                print("1234567890")      # True
           
    def lister(self):
        """Lister toutes les salles de la table Professeurs"""
        datas = db.read_database(self.curseur, "Professeurs")
        if datas:
            print("Voici les informations enregistrées concernant les Professeurs:\n ")
            placeholders = ['|indexes','|id','|nom' ,"|prenom" ,'|tel' ,'|email']
            display_list_columns(placeholders)
            for data in datas:
                display_list_columns(data)
        else:
            print("\nAucun Professeur n'est encore enregistré.\n")

    def modifier(self):        
        """Modifier les infos d'un Professeur"""
        id_Professeur = is_empty("Entrer le id du Professeur a modifier: \n -->")
        if db.verify_data(self.curseur, "Professeurs", "id_prof", id_Professeur) :
            while True:
                print('\t','-'*8,"MENU MODIFIER PROFESSEUR",'-'*8)
                print('\t','-'*32)
                print("Veuillez choisir entre les parmi options de modification suivantes: ")
                print("1- Modifier le nom du professeur.")
                print("2- Modifier le prenom du professeur.")
                print("3- Modifier le telephone du professeur")
                print("4- Modifier l'email du professeur")
                print("5- Retour au menu Professeur.")
                print("6- Quitter le programme. ")

                choix = is_empty("Faites votre choix:\n -->")
                if choix == '1':
                    nom = is_empty("Entrer le nouveau nom du professeur (x pour quitter): \n -->")
                    if nom == 'x':
                        return  
                    else:
                        db.update_data(self.curseur, "Professeurs", "id_prof", id_Professeur,  nom_prof = nom) 
                        print("Mise a jour effectuée")

                elif choix == '2':
                    prenom = is_empty("Entrer le nouveau prenom du professeur: (x pour quitter)\n -->")
                    if prenom == 'x':
                        return
                    else:
                        db.update_data(self.curseur, "Professeurs", "id_prof", id_Professeur,  prenom_prof = prenom)
                        print("Mise a jour effectuée")

                elif choix == "3":
                    while True:
                        tel = is_empty("Entrer le nouveau telephone du prof: (x pour quitter)\n -->")
                        if tel == 'x':
                            return
                        elif is_valid_phone_number(tel):
                            db.update_data(self.curseur, "Professeurs", "id_prof", id_Professeur,  tel_prof = tel)
                            print("Mise a jour effectuée")
                            break
                        else:
                            print("Telephone invalide. Exemple de formats valide:")
                            print("(123) 456-7890")  # True
                            print("123-456-7890")    # True
                            print("123 456 7890")   # True
                            print("1234567890")      # True
                elif choix == '4':
                    while True:
                        email = is_empty("Entrer la npuvelle adresse mail du prof: \n -->")
                        if email == 'x':
                            return
                        elif is_valid_email(email):
                            db.update_data(self.curseur, "Professeurs", "id_prof", id_Professeur,  email = email)
                            print("Mise a jour effectuée")
                            break
                        else:
                            print("Email invalide.\nExemple: something@domain.com")
                elif choix == '5':
                    break #or return
                elif choix == '6':
                    exit()
                else:
                    print("Vous devez choisir un chiffre entre 1 a 6.")
        else:
            print("Ce professeur n'est pas enregistré dans la base de données.")

    def rechercher(self):
        """filtrer la table Salles"""
        while True:
            print('\t','-'*8,"MENU RECHERCHER PROFESSEUR",'-'*8)
            print('\t','-'*32)
            print("Pour faire une recherche par filtre , vous devez choisir entre les parmi options suivantes: ")
            print("1- Rechercher un professeur par son id.")
            print("2- Retour au menu Professeur.")
            print("3- Quitter le programme. ")
            choix = is_empty("Faites votre choix: \n -->")
            
            if choix == '1':
                prof = is_empty("Entrer l'id du professeur a afficher:\n --> ")
                if db.verify_data(self.curseur, "Professeurs", "id_prof", prof) == True:
                    datas = db.search_by_data(self.curseur, "Professeurs","id_prof", prof)
                    placeholders = ['|indexes','|id','|nom' ,"|prenom" ,'|tel' ,'|email']
                    display_list_columns(placeholders)
                    for data in datas:
                        display_list_columns(data)
                else:
                    print("Ce professeur n'est pas enregistré dans la base de données.")

            elif choix == '2':
                break

            elif choix == '3':
                exit()

            else:
                print("Entrée invalide, Veuillez choisir entre les options proposées.")

    def supprimer(self):
        """Supprime un professeur , et toutes ses occurences dans les autres tables."""
        prof = is_empty("Entrer l'id du professeur a supprimer:(x pour quitter)\n --> ")
        if prof == 'x':
            return
        elif db.verify_data(self.curseur, "Professeurs", "id_prof", prof):
            while True: 
                print(f"Etes-vous sur de vouloir supprimer le Professeur {prof}?")
                choix = is_empty("1- Supprimer 2- Annuler\n -->")
                if choix == '1':
                    db.delete_database(self.curseur, "Professeurs", "id_prof", prof)
                    print(f"Suppression du Professeur {prof} effectuée!")
                    break
                elif choix == '2':
                    break
                else:
                    print("Vous devez choisir entre les options 1 et 2.")
        else:
            print("Ce Professeur n'est pas enregistré dans la base de données.")
  
    def menu_professeur (self) :
        """Fonction affichant les options de gestion des Professeurs"""
        while True:
            print('\n\t','-'*32)        
            print('\t','-'*8,"MENU PROFESSEUR",'-'*8)
            print('\t','-'*32,'\n')        
            print("Bienvenue au menu des professeurs.")
            print("Veuillez choisir votre option.")
            print("1- Enregistrer un Professeur.")
            print("2- Lister les professeurs.")
            print("3- Rechercher un Professeur.")
            print("4- Modifier les informations d'un Professeur.")
            print("5- Supprimer un Professeur.")
            print("6- Retour au menu principal.")
            print("7- Quitter le programme.")
            try:
                choix = int(input("Veuillez choisir votre option.[1-7]: "))
            except Exception as e:
                print("Erreur veuiller entrer un entier valide: ", e)
            else:
                if choix < 1 or choix > 7:
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
