import gestion_des_entites.Gestion_admin as adm
import gestion_des_entites.Gestion_batiments as bat 
import gestion_des_entites.Gestion_salles as sal
import gestion_des_entites.Gestion_professeurs as prof
import gestion_des_entites.Gestion_cours as crs
import gestion_des_entites.Gestion_horaires as hor
from gestion_des_contraintes.contraintes import attendre_touche, clear_screen, banner

def menu_pricipal(adm_id):
    while True:
        clear_screen()
        banner()
        print(" " * 20,'\t','*'*32)
        print(" " * 20,'\t','*'*8,"MENU PRINCIPAL",'*'*8)
        print(" " * 20,'\t','*'*32)
        print(" " * 20,"Bienvenue au menu Principal.\n")
        print(" " * 20,"Veuillez choisir votre option.")
        print(" " * 20,"1- Gestion des batiments.")
        print(" " * 20,"2- Gestion des salles.")
        print(" " * 20,"3- Gestion des cours.")
        print(" " * 20,"4- Gestion des horaires.")
        print(" " * 20,"5- Gestion des Professeurs.")
        print(" " * 20,"6- Retour au menu Système.")
        print(" " * 20,"7- Fermer le programme.")
        try: 
            print(" " * 20,"Faites votre choix_1:\n ",)
            choix_1 = int(input("          -->"))
        except Exception as e:
            print(" " * 20,"Erreur, vous devez fournir un entier: ", e)
        else:
            if choix_1 < 1 or choix_1 > 7:
                print(" " * 20,"Veuillez choisir un chiffre entre 1 et 6")
            else:
                attendre_touche()
                clear_screen()
                if choix_1 == 1:
                    Batiment = bat.Gestion_Batiment(adm_id)
                    Batiment.menu_batiment()
                elif choix_1 == 2:
                    salle = sal.Gestion_Salle(adm_id)
                    salle.menu_salle()
                elif choix_1 == 3:
                    cours = crs.Gestion_Cours(adm_id)
                    cours.menu_cours()
                elif choix_1 == 4:
                    horaire = hor.Gestion_Horaire(adm_id)
                    horaire.menu_horaire()
                elif choix_1 == 5:
                    professeur = prof.Gestion_Professeur(adm_id)
                    professeur.menu_professeur()
                elif choix_1 == 6:
                    main()
                elif choix_1 == 7:
                    print(" " * 20,"Fermeture du programme.")
                    attendre_touche()
                    exit()

def main():
    """Fonction principale contenant les fonctionnalites basiques du systeme"""
    while True:
        clear_screen()
        banner()
        print(" " * 20,'\t','*'*32)
        print(" " * 20,'\t','-'*8,"MENU SYSTEME",'-'*8)
        print(" " * 20,'\t','*'*32)
        print(" " * 20,"Bienvenu au Système de Gestion des salles du CHCL.\n")
        print(" " * 20,"Comment voulez vous y acceder au systeme?")
        print(" " * 20,"1- Administrateur")
        print(" " * 20,"2- Invité")
        print(" " * 20,"3- Quitter\n ")
        choix_0 = input("            -->")

        if choix_0 == '1':
            clear_screen()
            admin = adm.Gestion_admin()
            adm_id = admin.menu_adm()
            if adm_id:
                menu_pricipal(adm_id)
                break
        elif choix_0 == '2':
            clear_screen()
            adm_id = False
            menu_pricipal(adm_id)
        elif choix_0 == '3':
            print(" " * 20,"Fermeture du programme.")
            attendre_touche()
            exit()
        else:
            print(" " * 20,"Vous devez choisir entre 1 et 2.")
                
if __name__ == '__main__':
    main()