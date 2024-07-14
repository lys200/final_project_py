"""Projet final de Python
Date de remise: 12 Juillet 2024
Nom des membres du Groupe:
BELCEUS Samienove R.
CHERELUS Solem
MORISSET Nherlyse
ST-PREUX Christine
"""

""""Ce fichier fait la gestion des batiments."""

import Databases_pack.database as db
from gestion_des_contraintes.contraintes import func_exit,afficher_texte_progressivement, is_integer, attendre_touche, clear_screen,banner, is_empty, afficher_entete, afficher_donnees


class Gestion_Batiment:
    """Class contenant les fonctions relative aux batiments."""

    #curseur = db.Connect_to_database("Gestion_des_salles.db")
    #db.initialize_db(curseur)
    #choix = 0
    def __init__(self, adm_id):
        """Methode de constructeur gerant les attributs du batiments."""
        self.connection_db = db.connect_to_database("Gestion_des_salles.db")
        self.adm_id = adm_id
        db.initialize_conn(self.connection_db)
  
    def enregistrer(self):
        """Enregistre un nouveau batiment."""
        while True:
            print(' '*20, "Entrer le nom du batiment[A-D]:")
            id_bat = is_empty("(x pour quitter)").upper()
            if id_bat == 'X':
                return
            elif id_bat in ['A', 'B', 'C', 'D']:
                break
            else:
                print(' '*20, "Le batiment doit etre A, B, C ou D.\n")
        # verifier que le id_batiment n'exsite pas deja dans la table Batiment
        is_batiment = db.search_by_data(self.connection_db, "batiments", "id_batiment", id_bat)
        # insertion des donnees dans la table batiments
        if is_batiment:
            print(' '*20, "Ce batiment est déja enregistré.")
        else:
            db.insert_data(self.connection_db, "Batiments", id_batiment = id_bat, nombre_etages = 3, salle_de_cours = 0)
            print(' '*20, "Par défaut, le nombre d'étages est fixé à 3 et le nombre de salle à 0.")
            print(' '*20, "Veuillez passer au menu salle pour enregistrer des salles dans le batiment de votre choix")
            print(' '*20, f"Le Batiment {id_bat} est enregistré aves succès.\n")
       
    def lister(self):
        """Lister toutes les lignes de la table Batiments."""
        datas = db.read_database(self.connection_db, "Batiments")
        if datas:
            print(' '*20, "Voici les infos enregistrées sur les batiments:\n ")
            columns= ['index', 'batiments', 'étages', 'salles']
            largeur, separateur = afficher_entete(columns)
            afficher_donnees(datas, largeur, separateur)
        else:
            print('\n',' '*20, "Aucun batiment n'est encore enregistré.")

    def rechercher(self):
        """Rechercher par filtre dans la table Batiments."""
        while True:
            clear_screen()
            banner()
            print(' '*20,'-'*32)
            print(' '*20,'-'*8, "MENU RECHERCHER",'-'*8)
            print(' '*20,'-'*32)
            print('\n',' '*20, "Pour faire une recherche par filtre, ")
            print(' '*20, "vous devez choisir parmi les options suivantes\n")
            print(' '*20, "1- Rechercher par id_batiment")
            print(' '*20, "2- Afficher les salles d'un batiment")
            print(' '*20, "3- Rechercher par nombre de salle")
            print(' '*20, "4- Retour au menu batiment.")
            print(' '*20, "5- Quitter le programme.")
            choix = is_empty("Faites votre choix [1-5]:")
            if choix == '1':
                print(' '*20, "Entrer l'id du Batiment a afficher:")
                id_batiment = is_empty("(x pour quitter)").upper()
                if id_batiment == "X":
                    return
                elif db.verify_data(self.connection_db, "Batiments", "id_batiment", id_batiment) == True:
                    datas = db.search_by_data(self.connection_db, "Batiments", "id_batiment", id_batiment)
                    columns= ['index', 'batiments', 'étages', 'salles']
                    largeur, separateur = afficher_entete(columns)
                    afficher_donnees(datas, largeur, separateur)
                else:
                    print(' '*20, "Ce batiment n'est pas enregistré dans la base de données.")
            elif choix == '2':
                print(' '*20, "Entrer l'id du batiment dont vous voulez afficher les salles:")
                id_batiment = is_empty("(x pour quitter)").upper()
                if id_batiment == "X":
                    return
                elif db.verify_data(self.connection_db, "Salles", "id_batiment", id_batiment):
                    datas = db.search_by_data(self.connection_db, "Salles", "id_batiment", id_batiment)
                    if datas:
                        print(' '*20, f"Voici les infos des salles se trouvant au batiment {id_batiment}. \n")
                        columns= ['index', 'Salles', 'numero', 'batiment', 'etage', 'nombre de siege']
                        largeur, separateur = afficher_entete(columns)
                        afficher_donnees(datas, largeur, separateur)
                else:
                    print(' '*20, "Aucune salle trouvée.")
            elif choix == '3':
                print(' '*20, "Entrer le nombre de salle:")
                nbre_salle = is_empty("(x pour quitter)")
                if nbre_salle == "x":
                    return
                if is_integer(nbre_salle):
                    datas = db.search_by_data(self.connection_db, "Batiments", "salle_de_cours", nbre_salle)
                    if datas:
                        print(' '*20, f"Voici les informations des batiments contenant {nbre_salle} salle(s).\n")
                        columns = ['index', 'batiments', 'étages', 'salles']
                        largeur, separateur = afficher_entete(columns)
                        afficher_donnees(datas, largeur, separateur)
                    else:
                        print(' '*20, f"Aucun batiment ne contient {nbre_salle} salle(s).")
                else:
                    print(' '*20, "Vous devez enter un entier.")
            elif choix == '4':
                break
            elif choix == '5':
                self.connection_db.close()
                func_exit()
            else:
                print(' '*20, "Vous devez choisir entre 1 a 5.")
            attendre_touche()

    def supprimer(self):
        """Methode permettant de supprimer un batiment."""
        print(' '*20, "Entrer l'id du Batiment a supprimer:")
        id_batiment = is_empty("(x pour quitter)").upper()
        if id_batiment == 'X':
            return
        if db.verify_data(self.connection_db, "Batiments", "id_batiment", id_batiment) == True:
            while True:
                print("\n\t\t\t\tATTENTION!")
                Warning_= f"La supression du batiment {id_batiment} va entrainer la supression de toutes les salles de ce batiment."
                Warning_1 = "La supression de ces salles vont entrainer la supression des horaires pour les cours qui y etaient programmés.\n"
                afficher_texte_progressivement(Warning_)
                afficher_texte_progressivement(Warning_1)
                print(' '*20, f"Etesvous sur de vouloir poursuivre la supression du batiment {id_batiment}?")
                choix = is_empty("1- Supprimer  2- Annuler")
                if choix == '1':
                    # suppression des salles de ce batiment
                    # recuperantion des id des ces salles
                    salles = db.search_by_data(self.connection_db, "Salles", "id_batiment", id_batiment)
                    if salles:
                        salles_to_delete = []
                        for salle in salles:
                            salles_to_delete.append(salle[1])

                        # supprimer les salles de la liste salle_to_delete dans une boucle
                        horaire_id = []
                        for id_ in salles_to_delete:
                            print(' '*20, f'suppresion de la salle {id_} du batiment {id_batiment}')
                            db.delete_database(self.connection_db, "Salles", "id_salle", id_)
                            # recuperer la liste des horaires de chaque salle
                            horaire_id.append((db.search_by_data(self.connection_db, "Horaire", "code_salle", id_))[0][0])
                        if horaire_id:
                    # supprimer chaque id de chaque sous liste
                            for id_list in horaire_id:  
                                print(' '*20, f"Supression d'horaire {id_} de la table horaires.")
                                db.delete_database(self.connection_db, "Horaire", "id", id_)
                    # suppression du batiment
                    db.delete_database(self.connection_db, "Batiments", "id_batiment", id_batiment)
                    print(' '*20, f"Suppression du batiment {id_batiment} et ses salles effectuée!")
                    break
                elif choix == '2':
                    break
                else:
                    print(' '*20, "Vous devez choisir entre l'option 1 et 2.")
        else:
            print(' '*20, "Ce batiment n'est pas enregistré dans la batabase.")

    def menu_batiment(self):
        """Fonction affichant les options de gestion des batiments."""
        while True:
            clear_screen()
            banner()
            print(' '*20, '-'*32)
            print(' '*20, '-'*8, "MENU BATIMENT", '-'*9)
            print(' '*20, '-'*32)
            print(' '*20, "Bienvenue au menu Batiments.\n")
            print(' '*20, "Veuillez choisir votre option.")
            print(' '*20, "1- Enregistrer un batiment.[admin]")
            print(' '*20, "2- Lister tous les batiments.")
            print(' '*20, "3- Rechercher les information d'un batiment.")
            print(' '*20, "4- Supprimer un batiment.[admin]")
            print(' '*20, "5- Retour au menu principal.")
            print(' '*20, "6- Quitter le programme.")
            try:
                choix = int(is_empty("Faite votre choix"))
            except Exception as e:
                print(' '*20, "Erreur veuiller entrer un entier valide: ", e)
            else:
                if choix < 1 or choix > 6:
                    print(' '*20, "Veuillez choisir un chiffre entre 1 et 6")
                else:
                    if self.adm_id:
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
                            self.supprimer()
                            attendre_touche()
                        elif choix == 5:
                            break
                        else:
                            self.connection_db.close()
                            func_exit()
                    else:
                        if choix == 1:
                            print(' '*20, "Accès interdit. Seuls les adm peuvent enregistrer.\n")
                            attendre_touche()
                        elif choix == 2:
                            self.lister()
                            attendre_touche()
                        elif choix == 3:
                            self.rechercher()
                            attendre_touche()
                        elif choix == 4:
                            print(' '*20, "Accès interdit. Les adm seuls peuvent supprimer.\n")
                            attendre_touche()
                        elif choix == 5:
                            break
                        else:
                            self.connection_db.close()
                            func_exit()
