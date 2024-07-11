from time import sleep

def afficher_texte_progressivement(texte, delai=0.06):
    """
    Affiche le texte progressivement caractère par caractère.
    
    :param texte: Le texte à afficher.
    :param delai: Le délai en secondes entre chaque caractère (par défaut 0.1 seconde).
    """
    for caractere in texte:
        print(caractere, end='', flush=True)
        sleep(delai)
    print()  # Pour passer à la ligne suivante après l'affichage complet du texte

# Exemple d'utilisation
texte = "Gestion des salles du CHCL\n je suis mette ncndkejfnlevnl\n jbdickelievklnknflk"

afficher_texte_progressivement(texte, 0.01)
