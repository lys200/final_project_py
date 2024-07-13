"""Projet final de Python 
Date de remise: 12 Juillet 2024
Nom des membres du Groupe:
BELCEUS Samienove R.
CHERELUS Solem
MORISSET Nherlyse
ST-PREUX Christine
"""

import Databases_pack.database as db
from gestion_des_contraintes.contraintes import banner, afficher_entete, afficher_donnees, is_empty, is_valid_email, is_valid_phone_number, clear_screen, attendre_touche, Person, afficher_texte_progressivement
'''id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_prof TEXT PRYMARY KEY, 
                nom_prof TEXT NOT NULL,
                prenom_prof TEXT NOT NULL,
                tel_prof TEXT NOT NULL,
                email TEXT NOT NULL'''

class Gestion_Professeur:
    """Class contenant toutes les fonctions relative a la gestion des Salles."""
    
    def __init__(self, adm_id):
        """Methode constructeur pour la classe professeur."""
        self.connection = db.connect_to_database("Gestion_des_salles.db")
        self.adm_id = adm_id
        self.personne = Person()
        db.initialize_conn(self.connection)
        
    def enregistrer(self):
        """Enregistre un nouveau professeur."""
        nom = self.personne.f_name()
        if nom.lower() == 'x':
            return   
        prenom = self.personne.l_name()
        if prenom.lower() == 'x':
            return
        email = self.personne.mail()
        if not email:
            return
        while True:
            tel = is_empty("Entrer le telephone du prof: (x pour quitter)")
            if tel == 'x':
                return
            elif is_valid_phone_number(tel):
                db.insert_data(self.connection, "Professeurs", nom_prof = nom, prenom_prof = prenom, tel_prof = tel, email = email)
                print(' '*20, f"Le professeur {nom} {prenom} est enregistré avec succès.")
                break
            else:
                print(' '*20,"Telephone invalide. Exemple de formats valide:")
                print(' '*20,"(123) 456-7890")  # True
                print(' '*20,"123-456-7890")    # True
                print(' '*20,"123 456 7890")   # True
                print(' '*20,"1234567890")      # True
           
    def lister(self):
        """Lister toutes les salles de la table Professeurs."""
        datas = db.read_database(self.connection, "Professeurs")
        if datas:
            print(' '*20,"Voici les informations enregistrées concernant les Professeurs:\n ")
            placeholders = ['indexes','id du prof','nom du Prof' ,"prenom du prof" ,'telephone    ' ,'email du prof                  ']
            largeur, separateur = afficher_entete(placeholders)
            afficher_donnees(datas, largeur, separateur)
        else:
            print(' '*20,"\nAucun Professeur n'est encore enregistré.\n")

    def modifier(self):        
        """Modify les infos d'un Professeur."""
        id_Professeur = is_empty("Entrer le id du Professeur a modifier: ")
        if db.verify_data(self.connection, "Professeurs", "id_prof", id_Professeur) :
            while True:
                print('\t','-'*8,"MENU MODIFIER PROFESSEUR",'-'*8)
                print('\t','-'*32)
                print(' '*20,"Veuillez choisir entre les parmi options de modification suivantes: ")
                print(' '*20,"1- Modifier le nom du professeur.")
                print(' '*20,"2- Modifier le prenom du professeur.")
                print(' '*20,"3- Modifier le telephone du professeur")
                print(' '*20,"4- Modifier l'email du professeur")
                print(' '*20,"5- Retour au menu Professeur.")
                print(' '*20,"6- Quitter le programme. ")

                choix = is_empty("Faites votre choix:")
                if choix == '1':
                    nom = self.personne.l_name()
                    if nom.lower() == 'x':
                        return  
                    else:
                        db.update_data(self.connection, "Professeurs", "id_prof", id_Professeur,  nom_prof = nom) 
                        print(' '*20,"Mise a jour effectuée")

                elif choix == '2':
                    prenom = self.personne.f_name()
                    if prenom.lower() == 'x':
                        return
                    else:
                        db.update_data(self.connection, "Professeurs", "id_prof", id_Professeur,  prenom_prof = prenom)
                        print(' '*20,"Mise a jour effectuée")

                elif choix == "3":
                    while True:
                        tel = is_empty("Entrer le nouveau telephone du prof: (x pour quitter)")
                        if tel == 'x':
                            return
                        elif is_valid_phone_number(tel):
                            db.update_data(self.connection, "Professeurs", "id_prof", id_Professeur,  tel_prof = tel)
                            print(' '*20,"Mise a jour effectuée")
                            break
                        else:
                            print(' '*20,"Telephone invalide. Exemple de formats valide:")
                            print(' '*20,"(123) 456-7890")  # True
                            print(' '*20,"123-456-7890")    # True
                            print(' '*20,"123 456 7890")   # True
                            print(' '*20,"1234567890")      # True
                elif choix == '4':
                    while True:
                        email = self.personne.mail()
                        if email.lower() == 'x':
                            return
                        elif is_valid_email(email):
                            db.update_data(self.connection, "Professeurs", "id_prof", id_Professeur,  email = email)
                            print(' '*20,"Mise a jour effectuée")
                            break
                        else:
                            print(' '*20,"Email invalide. (Exemple: something@domain.com)")
                elif choix == '5':
                    break #or return
                elif choix == '6':
                    exit()
                else:
                    print(' '*20,"Vous devez choisir un chiffre entre 1 a 6.")
        else:
            print(' '*20,"Ce professeur n'est pas enregistré dans la base de données.")

    def rechercher(self):
        """Filtrer la table Salles."""
        while True:
            print(' '*20,'-'*32)
            print(' '*20,'-'*8,"MENU RECHERCHER PROFESSEUR",'-'*8)
            print(' '*20,'-'*32)
            print(' '*20,"Pour faire une recherche par filtre , vous devez choisir entre les parmi options suivantes: ")
            print(' '*20,"1- Rechercher un professeur par son id.")
            print(' '*20,"2- Retour au menu Professeur.")
            print(' '*20,"3- Quitter le programme. ")
            choix = is_empty("Faites votre choix: ")
            
            if choix == '1':
                prof = is_empty("Entrer l'id du professeur a afficher: ")
                if db.verify_data(self.connection, "Professeurs", "id_prof", prof) == True:
                    datas = db.search_by_data(self.connection, "Professeurs","id_prof", prof)
                    placeholders = ['indexes','id du prof','nom du Prof' ,"prenom du prof" ,'telephone    ' ,'email du prof                  ']
                    largeur, separateur = afficher_entete(placeholders)
                    afficher_donnees(datas, largeur, separateur)
                else:
                    print(' '*20,"Ce professeur n'est pas enregistré dans la base de données.")

            elif choix == '2':
                break

            elif choix == '3':
                exit()

            else:
                print(' '*20,"Entrée invalide, Veuillez choisir entre les options proposées.")

    def supprimer(self):
        """Supprime un professeur , et toutes ses occurences dans les autres tables."""
        prof = is_empty("Entrer l'id du professeur a supprimer:(x pour quitter) ")
        if prof == 'x':
            return
        elif db.verify_data(self.connection, "Professeurs", "id_prof", prof):
            while True: 
                Warning_= f"\t\t\t\tATTENTION!\n"
                Warning_1 = f"\tLa supression du {prof} va entrainer la supression de toutes les horaires pour les cours que dispensait le professeur."
                Warning_2 = "\t\tCar un cours ne peut pas etre dispensé sans professeur.\n"
                print(Warning_)
                afficher_texte_progressivement(Warning_1, 0.01)
                afficher_texte_progressivement(Warning_2, 0.01)
                print(' '*20,"Etes-vous sur de vouloir supprimer le Professeur {prof}?")
                choix = is_empty("1- Supprimer 2- Annuler")
                if choix == '1':
                    # recuperation  des cours dispense par le prof
                    cours = db.search_by_data(self.connection, "Cours", "id_prof", prof)
                    # recuperer les id de ces cours
                    horaire_to_delete = []
                    for crs in cours:
                        horaire_to_delete.append(crs[1])
                        # supprimer l'id du prof dans les donnees du cours
                        db.update_data(self.connection, "Cours", "id_cours", crs[1], id_prof = "----" )
                    print(horaire_to_delete)
                    
                    # supprimer les horaires de ces cours
                    
                    for id_ in horaire_to_delete:
                        print(' '*20, f"Suppression des horaires associées au cours: {id_}.")
                        db.delete_database(self.connection, "Horaire", "code_cours", id_)

                    db.delete_database(self.connection, "Professeurs", "id_prof", prof)
                    print(' '*20,f"Suppression du Professeur {prof} effectuée!")
                    break
                elif choix == '2':
                    break
                else:
                    print(' '*20,"Vous devez choisir entre les options 1 et 2.")
        else:
            print(' '*20,"Ce Professeur n'est pas enregistré dans la base de données.")
  
    def menu_professeur (self) :
        """Fonction affichant les options de gestion des Professeurs."""
        while True:
            clear_screen()
            banner()
            print(' '*20,'-'*32)        
            print(' '*20,'-'*8,"MENU PROFESSEUR",'-'*7)
            print(' '*20,'-'*32,'\n')        
            print(' '*20,"Bienvenue au menu des professeurs.")
            print(' '*20,"Veuillez choisir votre option.")
            print(' '*20,"1- Enregistrer un Professeur[admin].")
            print(' '*20,"2- Lister les professeurs.")
            print(' '*20,"3- Rechercher un Professeur.")
            print(' '*20,"4- Modifier les informations d'un Professeur[admin].")
            print(' '*20,"5- Supprimer un Professeur[admin].")
            print(' '*20,"6- Retour au menu principal.")
            print(' '*20,"7- Quitter le programme.")
            try:
                choix = int(is_empty("Veuillez choisir votre option.[1-7]: "))
            except Exception as e:
                print(' '*20,"Erreur veuiller entrer un entier valide: ", e)
            else:
                if choix < 1 or choix > 7:
                    print(' '*20,"Veuillez choisir un chiffre entre 1 et 7")
                else:
                    if self.adm_id :
                        if choix == 1:
                            self.enregistrer()
                            attendre_touche()
                        elif choix == 2:
                            self.lister()
                            attendre_touche()
                        elif choix == 3:
                            self.rechercher()
                            attendre_touche()
                        elif choix == 4:
                            self.modifier()
                            attendre_touche()
                        elif choix == 5:
                            self.supprimer()
                            attendre_touche()
                        elif choix == 6:
                            break  
                        else:
                            print(' '*20,"\n\tFermeture du programme...\n")
                            attendre_touche()
                            exit() 
                    else:
                        if choix == 1:
                            print(' '*20,"Accès interdit. Seuls les admins peuvent faire des enregistrements.\n")
                            attendre_touche()
                        elif choix == 2:
                            self.lister()
                            attendre_touche()
                        elif choix == 3:
                            self.rechercher()
                            attendre_touche()
                        elif choix == 4:
                            print(' '*20,"Accès interdit. Seuls les admins peuvent faire des modifications.\n")
                            attendre_touche()
                        elif choix == 5:
                            print(' '*20,"Accès interdit. Seuls les admins peuvent faire des suppressions.\n")
                            attendre_touche()
                        elif choix == 6:
                            break  
                        else:
                            print(' '*20,"Fermeture du programme...\n")
                            attendre_touche()
                            exit()
                    
