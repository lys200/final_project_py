""" Ici on trouve les codes concernant l'authentification de l'administrateur."""

import Databases_pack.database as db
from gestion_des_contraintes.contraintes import * 
class Gestion_admin:
    def __init__(self) -> None:
        self.curseur = db.connect_to_database("Gestion_des_salles.db")
        db.initialize_conn(self.curseur)
        self.adm_id = ""
        
    def Connection_adm(self):
        id_adm = is_empty("Entrer votre id: ")
        is_adm = db.search_by_data(self.curseur, "Administrateurs", "id_admin",id_adm,)
        if is_adm:
            mdp = is_empty("Entrer votre mot de passe: ")
            if hash_password(mdp) == is_adm[0][4]:
                return id_adm
            else:
                print("Mot de passe incorrect")
                return False
        else:
            print("Id invalide.")
            return False

    def new_adm_account(self):
        nom = is_empty("Entrer Votre nom: \n- ")
        prenom = is_empty("Entrer Votre prenom: \n")
        while True:
            password = is_empty("Entrer votre mot de passe:au moins[1 majuscule, 1 chiffre, et 1 caractere special, longueur =8 min] ")
            if is_valid_password(password):
                break
            else:
                print("Le mot de passe doit avoir au moins une majuscule, un chiffre et un caractère spécial.")
        hashed_password = hash_password(password)
        db.insert_data(self.curseur, "Administrateurs", nom_admin = nom, prenom_admin = prenom, password = hashed_password)
        print("-"*41)
        print(f"\nBienvenue {nom} {prenom}! Vous etes maintenant administrateurs. ")
        print("Une id vous a été attribuée. Veuillez afficher les admins pour récupérer le votre.\n")
        


    def show_adm_accounts(self):
        datas = db.read_database(self.curseur, "Administrateurs")
        if datas:
            print("\tVoici la liste des administrateurs enregistrés: ")
            print("\tIndex\t|id\t\t|Nom\t|Prenom\t|Password |")
            for data in datas:
                print("\t",data[0], "\t|", data[1], "|", data[2],"|", data[3],"|","********* |")
        else:
            print("Aucun administrateurs n'est encore enregistré.")
    
    def menu_adm (self):
        print('\n\t','-'*8,"MENU D'AUTHENTIFICATION",'-'*8)
        print('\t','-'*41)        
        adm_passkey = input("Entrer le code d'acces general: ").upper()
        if adm_passkey == "NO PAIN NO GAIN":
            while True:
                print("Bienvenue au menu d'authhentification.")
                print("1- Se connecter.")
                print("2- Creer un nouveau compte d'administrateur.")
                print("3- Afficher les administrateurs.")
                print("4- Quitter")
                choix = input("Faites votres choix: \n-")
                if choix in ['1','2','3','4']:
                    if choix == '1':
                        self.adm_id = self.Connection_adm()
                        break
                    elif choix == '2':
                        self.new_adm_account()

                    elif choix == '3':
                        self.show_adm_accounts()
                    else:
                        break
                else:
                    print("Entrée invalide: vous devez choisir entre les options 1 et 4")
        else:
            print("Code d'accès incorrect")
        return self.adm_id
