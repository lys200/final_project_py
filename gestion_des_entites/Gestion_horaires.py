"""CREATE TABLE IF NOT EXISTS Horaire (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code_cours TEXT NOT NULL,
                code_salle TEXT NOT NULL,
                jour TEXT NOT NULL,
                heure_debut INTEGER NOT NULL,
                heure_fin INTEGER NOT NULL,
                session INTEGER NOT NULL,
                annee INTEGER NOT NULL)
"""
"""Ce module contient les codes de gestions des horaires."""
import Databases_pack.database as db
from gestion_des_contraintes.contraintes import *

class Gestion_Horaire:
    """Cette class gère les codes de gestions des horaires."""
    
    def __init__(self, adm_id):
        self.connection_db = db.connect_to_database("Gestion_des_salles.db")
        self.adm_id = adm_id
        db.initialize_conn(self.connection_db)
        
    def enregistrer(self):
        """enregistre un cours dans l'horaire"""

        #recuperation du cours
        while True:
            print('\n', ' '*20,"entrer l'id du cours a enregistrer dans l'horaire:")
            cours = is_empty("(x pour quitter)")
            if cours.lower() == 'x':
                return
            elif db.verify_data(self.connection_db, "Cours", "id_cours", cours):
                cours_datas = db.search_by_data(self.connection_db, "Cours", "id_cours", cours)
                for data in cours_datas:
                    if data[5] == '----':
                        print(' '*20,f"Impossible de programmer le cours de {data[2]}, car il n'a pas encore d'enseignant.\n")
                        return
                else:
                    break
            else:
                while True:
                    print(' '*20,"Ce cours n'est pas enregistré dans la base de donnée.")
                    print(' '*20, "Veuillez l'enregistrer puis reassayer.")
                    ch = is_empty("1- reassayer\t2- abandonner l'enregistrement.")
                    if ch == '1':
                        break
                    elif ch == '2':
                        return
                    else:
                        print(' '*20,'Choisissez entre 1 et 2')

        #recuperation de la salle
        while True:
            print()
            salle = is_empty("Entrer l'id de la salle (x pour quitter): ").upper()
            if salle.lower() == 'x':
                return
            elif db.verify_data(self.connection_db, "Salles", "id_salle", salle):
                salle_datas = db.search_by_data(self.connection_db, "Salles", "id_salle", salle)
                break
            else:
                while True:
                    print(' '*20,"Cette salle n'est pas enregistrée dans la base de donnée.")
                    print(' '*20,"Veuillez l'enregistrer puis réessayer.")
                    ch = is_empty("1- réessayer 2- abandonner")
                    if ch == '1':
                        break
                    elif ch == '2':
                        return
                    else:
                        print(' '*20,'Choisissez entre 1 et 2')

        #recuperation des autre info jour/heure
        semaine = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi']
        while True:
            print()
            jour = is_empty("Entrer le jour(e.g., lundi) (x pour quitter):").lower()
            if jour == 'x':
                return
            elif jour in semaine:
                break
            else:
                print(' '*20,"Vous devez entrer un jour de la semaine, sauf dimanche.\n")

        #heure du debut
        while True:
            print('\n',' '*20,"Entrer l'heure de début du cours(HH:MM format 24h): ")
            debut = is_empty("(x pour quitter)")
            if debut.lower() ==  'x':
                return
            elif verifier_format_heure_v2(debut):
                if verifier_plage_horaire(debut):
                    #heure de la fin est généré automatiquement a partir de la duree du cours
                    duree = cours_datas[0][6]
                    #separer les heures des mns pour la duree
                    h1, m1 = map(int, duree.split(':'))
                    #separer les heures des mns pour l'heure du debut
                    h2, m2 = map(int, debut.split(':'))

                    #additionne les minutes
                    tot_minutes = m1+ m2
                    heure_additionnelles =  tot_minutes // 60
                    minutes_residuelles = tot_minutes % 60

                    tot_heures = h1 + h2 + heure_additionnelles

                    #ajuster l'heure finale au cas ou elle depasserait 24h bien qu'elle ne devrait pas
                    tot_heures = tot_heures % 24

                    heure_finale =  f"{tot_heures}:{minutes_residuelles}"
                    print(' '*20,f"L'heure finale est automatiquement générée --> {heure_finale}\n")
                    if verifier_plage_horaire(heure_finale):
                        break
                    else:
                        while True:
                            print(' '*20,"l'heure de fin ne doit pas exceder 16h, car c'est l'heure de fin des cours.")
                            print(' '*20,f" la duree du cours de {data[2]} est de {duree} h. CHoisissez le du debut en consequence.")
                            print(' '*20,"voulez-vous réessayer?")
                            ch = is_empty("1-oui\t2-abandonner")
                            if ch == '1':
                                break
                            elif ch == '2':
                                return
                            else:
                                print(' '*20,'Choisissez entre 1 et 2')

                else:
                    while True:
                        print(' '*20,"L'heure doit etre comprise entre 8:00 et 16:00.")
                        ch = is_empty("1-reassayer\t2- abandonner l'enregistrement")
                        if ch == '1':
                            break
                        elif ch == '2':
                            return
                        else:
                            print(' '*20,'Choisissez entre 1 et 2')
            else:
                while True:
                    print("Format d'heure invalide.")
                    print("1- réessayer         2- abandonner l'enregistrement")
                    ch = input(" --> ")
                    if ch == '1':
                        pass
                    elif ch == '2':
                        return
                    else:
                        print('Choisissez entre 1 et 2')

        #enregistrer l'annee
        while True:
            annee = is_empty("Entrer l'année accademique en cours (x pour quitter):").lower()
            if annee == 'x':
                return
            try:
                annee = int(annee)
                # Vérifier si l'annee est dans une plage raisonnable
                if annee >= 2024:
                    break
                else:
                    print(' '*20,"L'année doit être supérieure ou égale a l'année en cours(2024).\n")
            except ValueError:
                # Retourner False si l'entrée ne peut pas être convertie en entier
                print(' '*20,"Erreur: l'année doit être un entier.")
        
        #enregitrer la session
        while True:
            print('\n',' '*20,"Entrer la session pour laquelle vous enregistrez le cours dans l'horaire")
            session = is_empty("(x pour quitter)")
            if session == 'x':
                return
            elif session == '1' or session == '2':   
                session = int(session)             
                break
            else:
                print(' '*20,"la session doit etre 1 ou 2")

        #verifier que ces infos ne nonst pas deja enregistrees sinon enregistrer le cours dans l'horaire
        if  db.filter_table(self.connection_db, "Horaire", code_cours = cours, nom_cours = cours_datas[0][2], code_salle = salle, jour = jour, heure_debut = debut, heure_fin = heure_finale, session = session, annee = annee):
            print(' '*20,f"Le cours {cours} est deja enregistré dans l'horaire pour la {session}e session de l'annee {annee}.")
        else:
            if db.verifier_conflit(self.connection_db, jour, session, annee, debut, heure_finale, salle):
                print(' '*20,f"Il y a conflit entre l'horaire du cours {cours} et celle d'un autre cours, veuillez consulter l'horaire puis reassayer")
            else:
                db.insert_data(self.connection_db, "Horaire", code_cours = cours, nom_cours = cours_datas[0][2], code_salle = salle, jour = jour, heure_debut = debut, heure_fin = heure_finale, session = session, annee = annee)

    def modifier(self):        
        """Modifier les infos d'un Professeur"""
        id_horaire = is_empty("Entrer le id de l'horaire a modifier:(x pour quitter) ").lower()
        if id_horaire == 'x':
            return
        elif db.verify_data(self.connection_db, "Horaire", "id", id_horaire) :
            datas_h = db.search_by_data(self.connection_db, "Horaire", "id", id_horaire)
            print(datas_h)
            while True:
                clear_screen()
                banner()
                print("\tGestion Horaire")
                print('\t', '*'*15, '\n')
                print(' '*20,'-'*8,"MENU MODIFIER HORAIRE",'-'*8)
                print(' '*20,'-'*39)
                print()
                print(' '*20,"Veuillez choisir parmi les options de modification suivantes: ")
                print(' '*20,"1- Modifier la salle.")
                print(' '*20,"2- Modifier le jour du cours.")
                print(' '*20,"3- Modifier l'heure de debut du cours")
                print(' '*20,"4- Modifier la session")
                print(' '*20,"5- Modifier l'année")
                print(' '*20,"6- Retour au menu Horaire.")
                print(' '*20,"7- Quitter le programme. ")

                choix = is_empty("Faites votre choix [1-7]:")
                if choix == '1':
                    while True:
                        salle = is_empty("Entrer la nouvelle salle (x pour quitter): ").upper()
                        if salle == 'X':
                            return  
                        elif db.verify_data(self.connection_db, "Salles", "id_salle", salle):
                            if db.verifier_conflit(self.connection_db, datas_h[0][4], datas_h[0][7], datas_h[0][8], datas_h[0][5], datas_h[0][6], salle):
                                print(' '*20,f"Impossible de modifier l'horaire {id_horaire} pour la salle {salle}", 
                                        ' '*20, "car un autre cours de déroule dans cette salle.")
                            else:
                                db.update_data(self.connection_db, "Horaire", "id", id_horaire, code_salle = salle) 
                                print(' '*20,"Mise a jour effectuée")
                                break
                        else:
                            while True:
                                print(' '*20, "cette salle n'existe pas dans la base de données.")
                                print(' '*20, "1- Réessayer\t\t 2- Abandonner la modification")
                                ch = is_empty("Faites votre choix: ")
                                if ch == '1':
                                    break
                                if ch == '2':
                                    return
                                else:
                                    print(' '*20, "Vous devez choisir entre 1 et 2.")
              
                elif choix == '2':
                    while True:
                        jour = is_empty("Entrer le nouveau jour du cours (x pour quitter): ").lower()
                        if jour == 'x':
                            return  
                        elif jour in ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi']:
                            if db.verifier_conflit(self.connection_db,jour, datas_h[0][7], datas_h[0][8], datas_h[0][5], datas_h[0][6], datas_h[0][3]):
                                print(' '*20,f"Impossible de modifier l'horaire {id_horaire} pour {jour}", 
                                        ' '*20, "car un autre cours de déroule dans cette salle ce jour et a la meme heure.")
                            else:
                                db.update_data(self.connection_db, "Horaire", "id", id_horaire, code_salle = salle) 
                                print(' '*20,"Mise a jour effectuée")
                                break
                        else:
                            while True:
                                print(' '*20, "Vous devez entrer un jour de la semaine(sauf dimanche).")
                                print(' '*20, "1- réessayer\t\t 2- Abandonner la modification")
                                ch = is_empty("Faites votre choix: ")
                                if ch == '1':
                                    break
                                if ch == '2':
                                    return
                                else:
                                    print(' '*20, "Vous devez choisir entre 1 et 2.")
              
                elif choix == '3':
                    while True:
                        print(' '*20,"Entrer la nouvelle heure de début du cours(HH:MM format 24h):")
                        debut = is_empty("(x pour quitter)")
                        if debut.lower() ==  'x':
                            return
                        elif verifier_format_heure_v2(debut):
                            if verifier_plage_horaire(debut):
                                #heure de la fin est généré automatiquement a partir de la duree du cours
                                # generer la duree du cours
                                heure_h, minute_m = map(int, datas_h[0][5].split(':'))
                                heure1 = heure_h * 60 + minute_m
                                heure_h, minute_m = map(int, datas_h[0][6].split(':'))
                                heure2 = heure_h * 60 + minute_m

                                duree = heure2 - heure1
                                print (duree)
                                duree_str = f"0{duree//60}:{duree%60}"
                                #separer les heures des mns pour la duree
                                # h1, m1 = map(int, duree.split(':'))
                                h1 = duree // 60
                                m1 = duree % 60
                                print(h1, m1)                                #separer les heures des mns pour l'heure du debut
                                h2, m2 = map(int, debut.split(':'))
                                print(h2, m2)

                                #additionne les minutes
                                tot_minutes = m1+ m2
                                heure_additionnelles =  tot_minutes // 60
                                minutes_residuelles = tot_minutes % 60

                                tot_heures = h1 + h2 + heure_additionnelles

                                #ajuster l'heure finale au cas ou elle depasserait 24h bien qu'elle ne devrait pas
                                tot_heures = tot_heures % 24

                                heure_finale =  f"{tot_heures}:{minutes_residuelles}"
                                print(' '*20,f"L'heure finale est automatiquement générée--> {heure_finale}")
                                if verifier_plage_horaire(heure_finale):
                                    if db.verifier_conflit(self.connection_db, datas_h[0][4], datas_h[0][7], datas_h[0][8], debut, heure_finale, datas_h[0][3]):
                                        print(' '*20,f"Il y a conflit entre l'horaire du cours {datas_h[0][1]} et celle d'un autre cours, veuillez consulter l'horaire puis reassayer")
                                    else:
                                        db.update_data(self.connection_db, "Horaire", "id", id_horaire, heure_debut= debut)
                                        print(' '*20, "Modification effectuée!")
                                        break
                                else:
                                    while True:
                                        print(' '*20,"l'heure de fin ne doit pas exceder 16h, car c'est l'heure de fin des cours.")
                                        print(' '*20,f" la durée du cours de {datas_h[1]} est de {duree} h. Choisissez l'heure du début en conséquence.")
                                        print(' '*20,"voulez-vous réessayer?")
                                        ch = is_empty("1-oui\t2-non")
                                        if ch == '1':
                                            break
                                        elif ch == '2':
                                            self.modifier()
                                        else:
                                            print(' '*20,'Choisissez entre 1 et 2')

                            else:
                                while True:
                                    print(' '*20,"L'heure doit etre comprise entre 8:00 et 16:00.")
                                    ch = is_empty("1-Réessayer\t2- Abandonner la modification")
                                    if ch == '1':
                                        break
                                    elif ch == '2':
                                        return
                                    else:
                                        print(' '*20,'Choisissez entre 1 et 2')
                        else:
                            while True:
                                print("Format d'heure invalide.")
                                print("1- Réessayer         2- Abandonner la modification")
                                ch = input(" --> ")
                                if ch == '1':
                                    pass
                                elif ch == '2':
                                    return
                                else:
                                    print('Choisissez entre 1 et 2')

                elif choix == '4':
                    while True:
                        print('\n',' '*20,"Entrer la nouvelle session:")
                        session = is_empty("(x pour quitter):")
                        if session == 'x':
                            self.modifier()
                        elif session == '1' or session == '2':   
                            session = int(session)
                            if db.verifier_conflit(self.connection_db, datas_h[0][4], session, datas_h[0][8], datas_h[0][5], datas_h[0][6], datas_h[0][3]):
                                print(' '*20,f"Il y a conflit entre l'horaire du cours {datas_h[0][1]} et celle d'un autre cours, pour la session {session}")
                                print(' '*20, "veuillez consulter l'horaire puis reassayer")
                            else:
                                db.update_data(self.connection_db, "Horaire", "id", id_horaire, session= session)
                                print(' '*20, "Modification effectuée!")
                                break
                        else:
                            print(' '*20,"la session doit être 1 ou 2")

                elif choix == '5':
                     while True:
                        annee = is_empty("Entrer la nouvelle année accademique pour l'horaore du cours (x pour quitter):").lower()
                        if annee == 'x':
                            return
                        try:
                            annee = int(annee)                            
                        except ValueError:
                            # Retourner False si l'entrée ne peut pas être convertie en entier
                            print(' '*20,"Erreur: l'année doit être un entier.")
                        else: 
                            if annee >= 2024:
                                if db.verifier_conflit(self.connection_db, datas_h[0][4], datas_h[0][7], annee, datas_h[0][5], datas_h[0][6], datas_h[0][3]):
                                    print(' '*20,f"Il y a conflit entre l'horaire du cours {datas_h[0][1]} et celle d'un autre cours, pour l'année {annee}")
                                    print(' '*20, "veuillez consulter l'horaire puis reassayer")
                                else:
                                    db.update_data(self.connection_db, "Horaire", "id", id_horaire, annee= annee)
                                    print(' '*20, "Modification effectuée!")
                                    break
                            else:
                                print(' '*20,"l'année doit être supérieure ou égale a l'année en cours.") 

                elif choix == '6':
                    break
                elif choix == '7':
                    print(" "*20, "Fermeture du programme...")
                    attendre_touche()
                    exit()
                else:
                    print(" "*20, "Veuillez choisir un chiffre entre 1 et 7.\n")
                    attendre_touche()
                    
        else:
            print(' '*20,"Cette horaire n'est pas enregistrée dans la base de données.")
        attendre_touche()

    def lister(self):
        """Lister toutes les informations enregistreees dans l'horaire"""
        datas = db.read_database(self.connection_db, "Horaire")
        if datas:
            print(' '*20,"\tVoici les cours programmés dans l'horaire:\n ")

            placeholders = ['indexes','code du cours','nom du cours' ,"code de la salle" ,'  jour   ' ,'heure de début', 'heure de fin', 'session', 'année']
            largeur, separateur = afficher_entete(placeholders)
            afficher_donnees(datas, largeur, separateur)
        else:
            print("\n",' '*20,"Aucun cours n'est encore enregistré dans l'horaire.\n")

    def rechercher(self):
        """filtrer la table Salles"""
        while True:
            clear_screen()
            banner()
            print("\tGestion Horaire")
            print('\n','*'*15)
            print(' '*20,'-'*8,"MENU FILTRER HORAIRE",'-'*8)
            print(' '*20,'-'*38)
            print(' '*20,"Pour faire une recherche par filtre , vous devez choisir entre les parmi options suivantes: ")
            print(' '*20,"1- Rechercher une horaire par son id.")
            print(' '*20,"2- Afficher les horaires d'une salle.")
            print(' '*20,"3- Afficher les horaires d'un cours.")
            print(' '*20,"4- Afficher les horaires d'une faculte.")
            print(' '*20,"5- Afficher les horaires d'un batiment.")
            print(' '*20,"6- Trier les horaires par niveau.")
            print(' '*20,"7- Trier les horaires par session.")
            print(' '*20,"8- Trier les horaires par année.")
            print(' '*20,"9- retour au menu Horaire. ")
            print(' '*20,"10- Quitter le programme. ")
            choix = is_empty("Faites votre choix: ")
            
            if choix == '1':
                hor = is_empty("Entrer l'id de l'horaire a afficher: ")
                if db.verify_data(self.connection_db, "Horaire", "id", hor):
                    datas = db.search_by_data(self.connection_db, "Horaire","id", hor)
                    placeholders = ['indexes','code du cours','nom du cours' ,"code de la salle" ,'  jour   ' ,'heure de début', 'heure de fin', 'session', 'année']
                    largeur, separateur = afficher_entete(placeholders)
                    afficher_donnees(datas, largeur, separateur)
                else:
                    print(' '*20,"Cette horaire n'est pas enregistrée dans la base de données.")
            
            elif choix == '2':
                salle = is_empty("Entrer l'id de la salle dont vous voullez afficher l'horaire: ")
                if db.verify_data(self.connection_db, "Horaire", "code_salle", salle):
                    datas = db.search_by_data(self.connection_db, "Horaire","code_salle", salle)
                    placeholders = ['indexes','code du cours','nom du cours' ,"code de la salle" ,'  jour   ' ,'heure de début', 'heure de fin', 'session', 'année']
                    largeur, separateur = afficher_entete(placeholders)
                    afficher_donnees(datas, largeur, separateur)
                else:
                    print(' '*20,"Cette salle ne figure pas dans la table de l'horaire.")

            elif choix == '3':
                cours = is_empty("Entrer l'id du cours dont vous voullez afficher l'horaire: ")
                if db.verify_data(self.connection_db, "Horaire", "code_cours", cours):
                    datas = db.search_by_data(self.connection_db, "Horaire","code_cours", cours)
                    placeholders = ['indexes','code du cours','nom du cours' ,"code de la salle" ,'  jour   ' ,'heure de début', 'heure de fin', 'session', 'année']
                    largeur, separateur = afficher_entete(placeholders)
                    afficher_donnees(datas, largeur, separateur)
                else:
                    print(' '*20,"Ce cours ne figure pas dans la table de l'horaire.")

            elif choix == '4':
                fac = is_empty("Entrer la fac dont vous voulez afficher les horaires: ")

                datas = db.faire_jointure(self.connection_db, "Horaire", "cours", "code_cours", "id_cours", "Horaire.*", "cours.*", f"Cours.nom_fac = '{fac}'")
                
                if datas:
                    for data in datas:
                        display_list_columns(data)
                else:
                    print(' '*20,f"Aucune horaire n'est enregistrée pour les cours de la fac {fac}")
                # datas = db.search_by_data(self.connection_db, "Horaire","code_cours", salle)
                # placeholders = ['|indexes','|code du cours','|nom du cours' ,"|code de la salle" ,'|jour' ,'|heure de début', '|heure de fin', '|session', '|année']
                # display_list_columns(placeholders)
                # for data in datas:
                #     display_list_columns(data)

            elif choix == '5':
                bat = is_empty("Entrer l'id du cours dont vous voullez afficher l'horaire: ")
                if db.verify_data(self.connection_db, "Batiment", "id_batiment", bat):
                    datas = db.get_column_values_starting_with(self.connection_db, "Horaire", "code_salle", bat)
                    if datas:
                        placeholders = ['indexes','code du cours','nom du cours' ,"code de la salle" ,'  jour   ' ,'heure de début', 'heure de fin', 'session', 'année']
                        display_list_columns(placeholders)
                        for data in datas:
                            display_list_columns(data)
                    else:
                        print(' '*20,f"aucune horaire n'est encore enregistré pour le batiment {bat}")
                else:
                    print(' '*20,"Ce batiment n'est pas encore enregistré.")
 
            elif choix == '6':
                niveau = is_empty("Entrer le niveau dont vous voullez afficher les horaires: ")
                datas =  db.afficher_horaires(self.connection_db, niveau=niveau)
                if datas:
                    placeholders = ['indexes','code du cours','nom du cours' ,"code de la salle" ,'  jour   ' ,'heure de début', 'heure de fin', 'session', 'année']
                    largeur, separateur = afficher_entete(placeholders)
                    afficher_donnees(datas, largeur, separateur)
                else:
                    print(' '*20,"Aucune horaire n'est enregistré pour ce niveau.")

            elif choix == '7':
                session = is_empty("Entrer la session [1-2]: ")
                if session == '1' or session == '2':
                    datas = db.search_by_data(self.connection_db, "Horaire","session", session)
                    placeholders = ['indexes','code du cours','nom du cours' ,"code de la salle" ,'  jour   ' ,'heure de début', 'heure de fin', 'session', 'année']
                    largeur, separateur = afficher_entete(placeholders)
                    afficher_donnees(datas, largeur, separateur)
                else:
                    print(' '*20,"La session doit etre 1 ou 2.")

            elif choix == '8':
                while True:
                    try:
                        annee = int(is_empty("Entrer l'annee: (x pour quitter) "))
                    except ValueError: 
                        print(' '*20,"l'annee doit etre un entier.")
                    else: 
                        datas = db.search_by_data(self.connection_db, "Horaire","annee", annee)
                        if datas:
                            placeholders = ['indexes','code du cours','nom du cours' ,"code de la salle" ,'  jour   ' ,'heure de début', 'heure de fin', 'session', 'année']
                            display_list_columns(placeholders)
                            for data in datas:
                                display_list_columns(data)
                        else:
                            print(' '*20,f"Aucune horaire n'est enregistrée pour l'année {annee}.")
                        break
            elif choix == '9':
                break

            elif choix == '10':
                exit()

            else:
                print(' '*20,"Entrée invalide, Veuillez choisir entre les options proposées.")
            attendre_touche()
    
    def supprimer(self):
        """Supprime une horaire , et toutes ses occurences dans les autres tables."""
        hor = is_empty("Entrer l'id de l'horaire a supprimer:(x pour quitter) ")
        if hor == 'x':
            return
        elif db.verify_data(self.connection_db, "Horaire", "id", hor):
            while True: 
                print(' '*20,f"Etes-vous sur de vouloir supprimer cette info de l'horaire?")
                choix = is_empty("1- Supprimer 2- Annuler")
                if choix == '1':
                    db.delete_database(self.connection_db, "Horaire", "id", hor)
                    print(' '*20,f"Suppression de l'horaire {hor} effectuée!")
                    break
                elif choix == '2':
                    break
                else:
                    print(' '*20,"Vous devez choisir entre les options 1 et 2.")
        else:
            print(' '*20,"Cette id d'horaire n'est pas enregistré dans la base de données.")
  
    def menu_horaire (self) :
        """Fonction affichant les options de gestion des Professeurs"""
        while True:
            clear_screen()
            banner()
            print(' '*20,'-'*32)        
            print(' '*21,'-'*8,"MENU HORAIRE",'-'*8)
            print(' '*20,'-'*32,'\n')        
            print(' '*20,"Bienvenue au menu de l'horaire.")
            print(' '*20,"Veuillez choisir votre option.")
            print(' '*20,"1- Enregistrer un cours dans l'horaire [admin].")
            print(' '*20,"2- Afficher tous les horaires.")
            print(' '*20,"3- Rechercher une horaire.")
            print(' '*20,"4- Modifier une information dans l'horaire[admin].")
            print(' '*20,"5- Supprimer un cours de l'horaire[admin].")
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
                            clear_screen()
                        elif choix == 2:
                            while True:
                                clear_screen()
                                banner()
                                print(" "*20, "----AFFICHER HORAIRE----\n")
                                print(' '*20,"1- Afficher la liste générale des horaires.")
                                print(' '*20,"2- Afficher la grille des horaires, triées par session, niveau et faculté.")
                                choix = is_empty("Faites un choix: ")
                                if choix == '1':
                                    clear_screen()
                                    banner()
                                    self.lister()
                                    break
                                elif choix == '2':
                                    clear_screen()
                                    banner()
                                    print(' '*20, "Voici la grille des horaires, triées par session, niveau et faculté. ")
                                    db.afficher_horaire(self.connection_db)
                                    break
                                else:
                                    print(' '*20, "Veuillez choisir entre 1 et 2.")
                            attendre_touche()
                        elif choix == 3:
                            self.rechercher()
                        elif choix == 4:
                            self.modifier()
                        elif choix == 5:
                            self.supprimer()
                        elif choix == 6:
                            break  
                        else:
                            print(' '*20,"\tFermeture du programme...\n")
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
                            print(' '*20,"\tFermeture du programme...\n")
                            attendre_touche()
                            exit()
