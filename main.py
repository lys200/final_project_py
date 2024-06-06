import gestion_des_entites.Gestion_admin as adm
import gestion_des_entites.Gestion_batiments as bat 
import gestion_des_entites.Gestion_salles as sal

def menu_pricipal(adm_id):
    print(adm_id, 'id menu principal')
    while True:
        print('\t','*'*32)
        print('\t','*'*8,"MENU PRINCIPAL",'*'*8)
        print('\t','*'*32)
        print("Bienvenue au menu Principal.")
        print("Veuillez choisir votre option.")
        print("1- Gestion des batiments.")
        print("2- Gestion des salles.")
        print("3- Gestion des cours.")
        print("4- Gestion des horaires.")
        print("5- Gestion des Professeurs.")
        print("6- Retour au menu Système.")
        print("7- Fermer le programme.")
        try: 
            choix_1 = int(input("Faites votre choix_1: "))
        except Exception as e:
            print("Erreur, vous devez fournir un entier: ", e)
        else:
            if choix_1 < 1 or choix_1 > 7:
                print("Veuillez choisir un chiffre entre 1 et 6")
            else:
                if choix_1 == 1:
                    Batiment = bat.Gestion_Batiment(adm_id)
                    Batiment.menu_batiment()
                elif choix_1 == 2:
                    salle = sal.Gestion_Salle(adm_id)
                    salle.menu_salle()
                elif choix_1 == 3:
                    pass
                elif choix_1 == 4:
                    pass
                elif choix_1 == 5:
                    pass
                elif choix_1 == 6:
                    main()
                elif choix_1 == 7:
                    print("Fermeture du programme.")
                    exit()

def main():
    """Fonction principale contenant les fonctionnalites basiques du systeme"""
    print('\t','*'*32)
    print('\t','-'*8,"MENU SYSTEME",'-'*8)
    print('\t','*'*32)
    print("Bienvenu au Système de Gestion des salles du CHCL.")
    while True:
        print("Comment voulez vous y acceder au systeme?")
        choix_0 = input("1- Administrateur\t\t2- Invité \t\t 3- Quitter\n- ")
        if choix_0 == '1':
            admin = adm.Gestion_admin()
            adm_id = admin.menu_adm()
            print(adm_id)
            if adm_id:
                menu_pricipal(adm_id)
                break
        elif choix_0 == '2':
            adm_id = False
            menu_pricipal(adm_id)
        elif choix_0 == '3':
            exit()
        else:
            print("Vous devez choisir entre 1 et 2.")
                
if __name__ == '__main__':
    main()