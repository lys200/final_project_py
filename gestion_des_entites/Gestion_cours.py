import Databases_pack.database as db
from gestion_des_contraintes.contraintes import is_empty,attendre_touche, verifier_format_heure_v2,display_list_columns, afficher_texte_progressivement , afficher_entete, afficher_donnees
"""CREATE TABLE IF NOT EXISTS Cours (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cours TEXT, 
                nom_cours TEXT NOT NULL,
                id_prof TEXT NOT NULL,
                nom_fac TEXT,
                duree TEXT NOT NULL)
        """ 
class Gestion_Cours:
    """Class contenant toutes les fonctions relative a la gestion des Salles"""
    
    def __init__(self, adm_id):
        self.curseur = db.connect_to_database("Gestion_des_salles.db")
        self.adm_id = adm_id
        db.initialize_conn(self.curseur)
        
    def enregistrer(self):
        """Enregistre un nouveau cours"""
        nom = is_empty("Entrer le nom du cours:(x pour quitter).")
        if nom.lower() == 'x':
            return
        
        fac = is_empty("Entrer la filière dans laquelle se dispense le cours: (x pour quitter)")
        # Dictionnaire des filières enseignées au Campus Henry Christophe de Limonade (CHCL)
        filieres_chcl = {
            "Sciences de la Santé": ["Médecine", "Pharmacie", "Biologie médicale", "Soins infirmiers"],
            "Sciences Agronomiques": ["Agronomie", "Sciences animales", "Génie rural"],
            "Sciences de l'Ingénieur": ["Génie civil", "Génie électrique", "Génie mécanique", "Génie industriel"],
            "Sciences Économiques et Administratives": ["Gestion des affaires", "Économie", "Comptabilité", "Finance"],
            "Sciences Sociales et Humaines": ["Sociologie", "Psychologie", "Anthropologie", "Travail social"],
            "Lettres et Sciences Humaines": ["Langues et littératures", "Histoire", "Géographie", "Philosophie"],
            "Sciences de l'Éducation": ["Pédagogie", "Administration scolaire"],
            "Sciences Informatiques": ["Informatique", "Technologie de l'information"]
            }
        while True:
            try:
                niveau = is_empty("Entrer le niveau dans lequel sera enseigné le cours(x pour quitter)")
                if niveau == 'x':
                    return
                else:
                    niveau = int(niveau)
            except Exception as e:
                print(' '*20,"L'entrée doit etre un chiffe: ", e)
            else:  
                if niveau < 1 or niveau > 7:
                    print(' '*20,"le niveau doit etre de 1 a 7.")
                else:
                    break
        id_crs = f"{nom[0:3]}_{fac[0:3]}_L{str(niveau)}"
        if db.verify_data(self.curseur, "Cours", "id_cours", id_crs):
            print(' '*20,f"Le cours de {nom} est deja enregistré pour le niveau L{niveau} en {fac}.")
        else:
            while True: 
                print('\n',' '*20,"Entrer l'id du professeur qui dispense ce cours:")
                print(' '*20,"2- si le cours n'a pas encore de prof.")
                prof = is_empty("x pour quitter")
                if prof == '2' :
                    prof = "----"
                    break
                elif prof.lower() == 'x':
                    return
                #verifier que le id_prof exsite  deja dans la table Professeurs
                else:
                    is_prof = db.search_by_data(self.curseur, "Professeurs", "id_prof", prof)
                    #insertion des donnees dans la table batiments
                    if not is_prof:
                        print(' '*20,f"Le professeur {is_prof} n'est pas enregistré dans la table des professeurs.")
                        print(' '*20,"Veuillez d'abord l'enregistrer dans le menu 'Professeurs'.\n")
                        ch = is_empty("1- Reessayer 2-Abandonner l'enregistrement")
                        if ch == "1":
                            pass
                        elif ch == '2':
                            return
                        else:
                            print(' '*20,"Vous devez choisir entre 1 et 2.")
                    else:
                        break

            while True:
                print(' '*20,"Entrer la durée du cours(HH:MM format 24h): ")
                duree = is_empty("(x pour quitter)")
                if duree.lower() ==  'x':
                    return
                elif verifier_format_heure_v2(duree):
                    heure_h, minute_m = map(int, duree.split(':'))
                    total_minutes = heure_h * 60 + minute_m
                    if (total_minutes > 60) and (total_minutes < 360):
                        db.insert_data(self.curseur, 'Cours', nom_cours = nom, nom_fac = fac, niveau = niveau, id_prof = prof, duree = duree)
                        break
                    else:
                        while True:
                            print(' '*20,"La durée ne doit pas etre inferieure a 1h ou superieure a 6h.")
                            ch = input("1- reassayer         2- abandonner l'enregistrement")
                            if ch == '1':
                                break
                            elif ch == '2':
                                return
                            else:
                                print(' '*20,'Choisissez entre 1 et 2')
                else:
                    while True:
                        print(' '*20,"Format d'heure invalide.")
                        print(' '*20,"1- reassayer         2- abandonner l'enregistrement")
                        ch = input(" --> ")
                        if ch == '1':
                            break
                        elif ch == '2':
                            return
                        else:
                            print(' '*20,'Choisissez entre 1 et 2')
                    
    def lister(self):
        """Lister tous les Cours de la table Cours"""
        datas = db.read_database(self.curseur, "Cours")
        if not datas:
            print("\n", ' '*20,"Aucun cours n'est encore enregistré.\n")
        else:
            print(' '*20,"Voici les informations enregistrées concernant les Cours:\n ")
            columns = ['Index','Id du cours','nom cours' ,"   Faculté   " ,'Niveau' ,'Id_prof', 'Durée']
            largeur, separateur = afficher_entete(columns)
            afficher_donnees(datas, largeur, separateur)
            

    def modifier(self):        
        """Modifier les infos d'un cours"""
        id_cours = is_empty("Entrer le id du cours a modifier (x pour quitter):")
        if id_cours == 'x':
            return
        elif db.verify_data(self.curseur, "Cours", "id_cours", id_cours) :
            while True:
                print(' '*20,'-'*8,"MENU MODIFIER Cours",'-'*8)
                print(' '*20,'-'*32)
                print(' '*20,"Veuillez choisir entre les parmi options de modification suivantes: ")
                print(' '*20,"1- Modifier l'id du professeur.")
                print(' '*20,"2- Modifier la durée du cours.")
                print(' '*20,"3- Retour au menu Cours.")
                print(' '*20,"4- Quitter le programme. ")

                choix = is_empty("Faites votre choix:")
                if choix == '1':
                    while True:
                        prof = is_empty("Entrer le nouveau id du professeur\n(x pour quitter): ")
                        if prof == 'x':
                            break  
                        elif db.verify_data(self.curseur, "Professeurs", "id_prof", prof):
                            #insertion du nouveau prof dans la table cours
                            db.update_data(self.curseur, "Cours", "id_cours", id_cours, id_prof = prof)
                            break
                        else:
                                print("\n",' '*20,f"Le professeur {prof} n'est pas enregistré dans la table des professeurs.")
                                print(' '*20,"Veuillez d'abord l'enregistrer dans le menu 'Professeurs'.\n")
                                while True:
                                    ch = is_empty("1- Réessayer\t 2-Abandonner la modification.")
                                    if ch == "1":
                                        break
                                    elif ch == '2':
                                        return
                                    else:
                                        print(' '*20,"Vous devez choisir entre 1 et 2.")

                elif choix == '2':      
                    while True:
                        print(' '*20,"Entrer la nouvelle durée du cours(HH:MM format 24h): ")
                        duree = is_empty("(x pour quitter)")
                        if duree.lower() ==  'x':
                            return
                        elif verifier_format_heure_v2(duree):
                            heure_h, minute_m = map(int, duree.split(':'))
                            total_minutes = heure_h * 60 + minute_m
                            if total_minutes > 60 and total_minutes < 360:
                                db.update_data(self.curseur, "Cours", 'id_cours', id_cours, duree = duree)
                                break
                            else:
                                print(' '*20,"La durée ne doit pas etre inferieure a 1h ou superieure a 6h.")
                                while True:
                                    ch = is_empty("1- réessayer         2- Abandonner la modification")
                                    if ch == "1":
                                        break
                                    elif ch == '2':
                                        return
                                    else:
                                        print(' '*20,"Vous devez choisir entre 1 et 2.")
                        else:
                            while True:
                                print(' '*20,"Format d'heure invalide.")
                                ch = input("1- réessayer         2- abandonner la modification")
                                if ch == '1':
                                    break
                                elif ch == '2':
                                    return
                                else:
                                    print(' '*20,'Choisissez entre 1 et 2')

                elif choix == "3":
                    break #or return
                elif choix == '4':
                    print(' '*20,"Fermeture du programme...")
                    attendre_touche()
                    exit()
                else:
                    print(' '*20,"Vous devez choisir un chiffre compris entre 1 et 4.")
        else:
            print(' '*20,"Ce cours n'est pas enregistré dans la base de données.")

    def rechercher(self):
        """filtrer la table cours"""
        while True:
            print(' '*20,'-'*8,"MENU RECHERCHER COURS",'-'*8)
            print(' '*20,'-'*32)
            print(' '*20,"Pour faire une recherche par filtre , vous devez choisir entre les parmi options suivantes: ")
            print(' '*20,"1- Rechercher un Cours par son id.")
            print(' '*20,"2- Afficher les cours par nom.")
            print(' '*20,"3- Afficher les cours par faculté.")
            print(' '*20,"4- Afficher les cours par niveau.")
            print(' '*20,"5- Afficher les cours par professeur.")
            print(' '*20,"6- Afficher les cours par durée.")
            print(' '*20,"7- Retour au menu cours.")
            print(' '*20,"8- Quitter le programme.")
            choix = is_empty("Faites votre choix: ")
            
            if choix == '1':
                while True:
                    cours = is_empty("Entrer l'id du cours a afficher (x pour quitter):  ")
                    if cours == 'x':
                        break
                    elif db.verify_data(self.curseur, "Cours", "id_cours", cours):
                        datas = db.search_by_data(self.curseur, "Cours","id_cours", cours)
                        columns = ['Index','Id du cours','nom cours' ,"   Faculté   " ,'Niveau' ,'Id_prof', 'Durée']
                        largeur, separateur = afficher_entete(columns)
                        afficher_donnees(datas, largeur, separateur)
                        break
                    else:
                        print(' '*20,f"Le Cours d'id {cours} n'est pas enregistré dans la base de données.")

            elif choix == '2':
                while True:
                    nom = is_empty("Entrer le nom a afficher (x pour quitter): ")
                    if nom == 'x':
                        break
                    elif db.verify_data(self.curseur, "Cours", "nom_cours", nom):
                        datas = db.search_by_data(self.curseur, "Cours","nom_cours", nom)
                        columns = ['Index','Id du cours','nom cours' ,"   Faculté   " ,'Niveau' ,'Id_prof', 'Durée']
                        largeur, separateur = afficher_entete(columns)
                        afficher_donnees(datas, largeur, separateur)
                        break
                    else: 
                        print(' '*20,f"Le cours {nom} n'est encore enregistré dans la base de donn♪es.")

            elif choix == '3':
                while True:
                    fac = is_empty("Entrer la faculté dont vous vouller afficher les cours (x pour quitter): ")
                    if fac == 'x':
                        break
                    elif db.verify_data(self.curseur, "Cours", "nom_fac", fac):
                        datas = db.search_by_data(self.curseur, "Cours","nom_fac", fac)
                        columns = ['Index','Id du cours','nom cours' ,"   Faculté   " ,'Niveau' ,'Id_prof', 'Durée']
                        largeur, separateur = afficher_entete(columns)
                        afficher_donnees(datas, largeur, separateur)
                        break
                    else: 
                        print(' '*20,f"Aucun cours n'est encore enregistré pour la faculté de {fac}.")
            
            elif choix == '4':
                while True:
                    level = is_empty("Entrer le niveau dont vous vouller afficher les cours (x pour quitter): ")
                    if level == 'x':
                        break
                    elif db.verify_data(self.curseur, "Cours", "niveau", level):
                        datas = db.search_by_data(self.curseur, "Cours","niveau", level)
                        columns = ['Index','Id du cours','nom cours' ,"   Faculté   " ,'Niveau' ,'Id_prof', 'Durée']
                        largeur, separateur = afficher_entete(columns)
                        afficher_donnees(datas, largeur, separateur)
                        break
                    else: 
                        print(' '*20,f"Aucun cours n'est encore enregistré pour le niveau {level}.")
            
            elif choix == '5':
                while True:
                    prof = is_empty("Entrer l'id du professeur dont vous vouller afficher les cours (x pour quitter): ")
                    if prof == 'x':
                        break
                    elif db.verify_data(self.curseur, "Cours", "id_prof", prof):
                        print (' '*20,f"\t\tLes cours du niveau {prof} sont les suivants: ")
                        datas = db.search_by_data(self.curseur, "Cours","id_prof", prof)
                        columns = ['Index','Id du cours','nom cours' ,"   Faculté   " ,'Niveau' ,'Id_prof', 'Durée']
                        largeur, separateur = afficher_entete(columns)
                        afficher_donnees(datas, largeur, separateur)
                        break
                    else: 
            
                        print(' '*20,f"Aucun cours n'est enseigné pas le prof {prof}.")
            
            elif choix == '6':
                while True:
                    print(' '*20,"Entrer la durée des cours que vous voulez afficher (HH:MM format 24h)")
                    duree = is_empty("(x pour quitter): ").lower()
                    if duree == 'x':
                        break
                    else:
                        if verifier_format_heure_v2(duree):
                            if db.verify_data(self.curseur, "Cours", "duree", duree):
                                print (' '*20,f"\t\tLes cours de durrée {duree} sont les suivants: ")
                                datas = db.search_by_data(self.curseur, "Cours","duree", duree)
                                columns = ['Index','Id du cours','nom cours' ,"   Faculté   " ,'Niveau' ,'Id_prof', 'Durée']
                                largeur, separateur = afficher_entete(columns)
                                afficher_donnees(datas, largeur, separateur)
                                break
                            else: 
                                print(' '*20,f"Aucun cours ne dure {duree} heure(s).")
                        else:
                            while True:
                                print(' '*20,"Format d'heure invalide.")
                                ch = input("1- réessayer         2- abandonner la recherche")
                                if ch == '1':
                                    break
                                elif ch == '2':
                                    return
                                else:
                                    print(' '*20,'Choisissez entre 1 et 2')
            elif choix == '7':
                break
            
            elif choix == '8':
                print(' '*20,"Fermeture du programme...")
                attendre_touche()
                exit()

            else:
                print(' '*20,"Entrée invalide, Veuillez choisir entre les options proposées.")

    def supprimer(self):
        """Supprime un cours, et toutes ses occurences dans les autres tables."""
        id_cours = is_empty("Entrer l'id du cours a supprimer:(x pour quitter) ")
        if id_cours == 'x':
            return
        elif db.verify_data(self.curseur, "Cours", "id_cours", id_cours):
            while True: 
                Warning_= f"\t\t\t\tATTENTION!\n"
                Warning_1 = f"La supression du cours {id_cours} va entrainer la supression de toutes les horaires enregistrées pour ce cours.\n"
                print(Warning_)
                afficher_texte_progressivement(Warning_1, 0.02)
                print(' '*20,f"Etes-vous sur de vouloir supprimer le Cours {id_cours}?")
                choix = is_empty("1- Supprimer \t2- Annuler")
                if choix == '1':
                    # recuperation des horaires de ce cours
                    horaires = db.search_by_data(self.curseur, "Horaire", "code_cours", id_cours)                    
                    horaires_to_del = []
                    for horaire in horaires:
                        horaires_to_del.append(horaire[0])
                    # supression des horaires
                    for id_ in horaires_to_del:
                        print(' '*20, f"Suppression de l'horaire {id_} de la base de données")
                        db.delete_database(self.curseur, "Horaire", "id", id_)
                    # suppression du cours 

                    db.delete_database(self.curseur, "Cours", "id_cours", id_cours)
                    print(' '*20,f"Suppression du cours {id_cours} effectuée!")
                    break
                elif choix == '2':
                    break
                else:
                    print(' '*20,"Vous devez choisir entre les options 1 et 2.")
        else:
            print(' '*20,"Ce cours n'est pas enregistré dans la base de données.")
  
    def menu_cours (self) :
        """Fonction affichant les options de gestion des Cours"""
        while True:
            print('\n\t','-'*32)        
            print('\t','-'*8,"MENU COURS",'-'*8)
            print('\t','-'*32,'\n')        
            print(' '*20,"Bienvenue au menu des cours.")
            print(' '*20,"Veuillez choisir votre option.\n")
            print(' '*20,"1- Enregistrer un cours.")
            print(' '*20,"2- Lister les cours.")
            print(' '*20,"3- Rechercher un cours.")
            print(' '*20,"4- Modifier les informations d'un cours.")
            print(' '*20,"5- Supprimer un cours.")
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
