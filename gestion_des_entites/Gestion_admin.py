"""Projet final de Python 
Date de remise: 12 Juillet 2024
Nom des membres du Groupe:
BELCEUS Samienove R.
CHERELUS Solem
MORISSET Nherlyse
ST-PREUX Christine
"""

"""Ici on trouve les codes concernant l'authentification de l'administrateur."""
import Databases_pack.database as db
from gestion_des_contraintes.contraintes \
    import banner,is_empty, hash_password,Person, \
        attendre_touche, clear_screen,is_valid_password, afficher_entete, afficher_donnees

class Gestion_admin(Person):
    """Classe gerant  les proprietes des administrateurs."""

    def __init__(self):
        """Constructeur de la classe dans lequel on passe les attributs."""
        self.curseur = db.connect_to_database("Gestion_des_salles.db")
        db.initialize_conn(self.curseur)
        self.adm_id = False

    def connection_adm(self):
        """Methode permettant de connecter des administrateurs."""
        while True:
            id_adm = is_empty("Entrer votre id(x pour quitter): ")

            if id_adm.lower() == 'x':
                return
            if db.verify_data(self.curseur, "Administrateurs", "id_admin", id_adm):
                is_adm = db.search_by_data(self.curseur, "Administrateurs", "id_admin",id_adm,)

                mdp = is_empty("Entrer votre mot de passe:(x pour quitter):")
                if mdp == 'x':
                    return
                if hash_password(mdp) == is_adm[0][4]:
                    print(' '*30,"Connexion reussie!")
                    print(' '*20,f"Bienvenue {is_adm[0][2]} {is_adm[0][3]}!")
                    return id_adm
                print('\n',' '*20,"Mot de passe incorrect")
                return False
            else:
                while True:
                    print('\n',' '*20,"Id invalide.")
                    print('\n',' '*20,"1- Reessayer    2- Abandonner.")
                    ch = is_empty("Faites un choix")
                    if ch == '1':
                        break
                    elif ch == '2':
                        return
                    else:
                        print('\n',' '*20,"Choix invalide.\n")


    def new_adm_account(self):
        """Methode permettant d'ajouter un nouveau administrateur."""
        personne = Person()
        nom = personne.f_name()
        if nom.lower() == 'x':
            return
        prenom = personne.l_name()
        if prenom.lower() == 'x':
            return
        #nom = is_empty("Entrer Votre nom: (x pour quitter) \n- ")
        #prenom = is_empty("Entrer Votre prenom: \n")
        while True:
            print('\n',' '*20,"Entrer votre mot de passe:\n",' '*20,\
                  "(au moins 1 majuscule, 1 chiffre, et 1 caractere special, longueur =8 min)")
            password = is_empty("(x pour quitter):")
            if password.lower() == 'x':
                return
            if is_valid_password(password):
                break
            print('\n',' '*15,"Le mot de passe doit avoir au moins une majuscule, un chiffre et un caractère spécial.")
        hashed_password = hash_password(password)
        db.insert_data(self.curseur, "Administrateurs", \
                       nom_admin = nom, prenom_admin = prenom, password = hashed_password)
        print("\n\n",'\n',' '*20,f"Bienvenue {nom} {prenom}! Vous etes maintenant administrateurs. ")
        print('\n',' '*20,"Une id vous a été attribuée. Veuillez afficher les admins pour récupérer le votre.")

    def show_adm_accounts(self):
        """Cette methode affiche les comptes des administrateurs."""
        datas = db.read_database(self.curseur, "Administrateurs")
        if datas:
            print("\t\t\tVoici la liste des administrateurs enregistrés: ")
            columns = ['Index', 'id de l\'admin', 'Nom de l\'admin', 'Prenom de l\'admin', 'Password ']
            cacher_mdp = [list(sublist[:-1]) + ["*********"] for sublist in datas]
            largeur, separateur = afficher_entete(columns)
            afficher_donnees(cacher_mdp, largeur, separateur)
        else:
            print(' '*20,"Aucun administrateur n'est encore enregistré.")

    def menu_adm (self):
        """Menu de Gestion des administrateurs."""
        banner()
        print(' '*20, '-'*8,"MENU D'AUTHENTIFICATION",'-'*8)
        print(' '*20,'-'*41)
        print("\n",' '*20,"Entrer le code d'acces general:")
        adm_passkey = input("\t\t--> ").upper()
        if adm_passkey == "NO PAIN NO GAIN":
            while True:
                clear_screen()
                banner()
                print(" " * 20,'-'*32)
                print(" " * 20,'-'*5,"MENU ADMINISTRATEUR.",'-'*5)
                print(" " * 20,'-'*32, '\n')
                print(" " * 20,"Bienvenue au menu des administrateurs.")
                print(" " * 20,"Veuillez choisir parmi les options ci-dessous.")
                print(" " * 20,"1- Se connecter.")
                print(" " * 20,"2- Creer un nouveau compte d'administrateur.")
                print(" " * 20,"3- Afficher les administrateurs.")
                print(" " * 20,"4- Quitter")
                choix = is_empty("Faites votres choix:")
                if choix in ['1','2','3','4']:
                    if choix == '1':
                        self.adm_id = self.connection_adm()
                        attendre_touche()
                        clear_screen()
                        break
                    if choix == '2':
                        self.new_adm_account()
                        attendre_touche()
                        clear_screen()
                    if choix == '3':
                        self.show_adm_accounts()
                        attendre_touche()
                        clear_screen()
                    else:
                        attendre_touche()
                        clear_screen()
                        break
                else:
                    print(" " * 15,"Entrée invalide: vous devez choisir entre les options 1 et 4")
                    attendre_touche()
                    clear_screen()
        else:
            print(" " * 15,"Code d'accès incorrect")
        return self.adm_id
