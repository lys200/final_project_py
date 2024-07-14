"""Projet final de Python 
Date de remise: 12 Juillet 2024
Nom des membres du Groupe:
BELCEUS Samienove R.
CHERELUS Solem
MORISSET Nherlyse
ST-PREUX Christine

Ce module contient les differents test de contraintes
"""
from datetime import datetime
import re
import hashlib
import os
from sys import platform
from time import sleep
from sys import exit

def banner():
    phrase = "Projet Gestion des salles du Campus Henry Chistophe de Limonade"
    longueur_phrase = len(phrase)
    print(" " * 10, "+" + "-" * (longueur_phrase + 2) + "+")
    print(" " * 10, "| " + phrase + " |")
    print(" " * 10, "+" + "-" * (longueur_phrase + 2) + "+")
    print("\n\n")


def func_exit():
    print('\n', ' '*20, "Fermeture du programme...")
    attendre_touche()
    exit()


def is_empty(input_message):
    """Verifie que le champs rempli par le user n'est pas vide."""
    while True:
        print(' '*20, input_message)
        user_input = input("                    -->").strip()
        if user_input:
            return user_input
        print(' ' * 20, "L'entrée ne peut pas être vide ou ne contenir"
                  "que des espaces. Veuillez réessayer.\n")


def is_integer(number):
    '''Verifie si un variable est de type int'''
    try:
        return isinstance(int(number), int)
    except ValueError:
        return False


def is_valid_password(password):
    """Verifie si le mot de passe a au moins une majuscule,
    un chiffre et un caractere special. """
    # (?=.*[A-Z]):  vérifie qu'il y a au moins
    # une lettre majuscule dans la chaîne.
    # (?=.*\d): vérifie qu'il y a au moins un chiffre dans la chaîne.
    # (?=.*[@$!%*?&]):  vérifie qu'il y a au moins un des
    # caractères spéciaux spécifiés dans la chaîne.
    # [A-Za-z\d@$!%*?&]{8,}: Cela assure que le mot de passe est composé
    # uniquement des caractères spécifiés (lettres, chiffres,
    # caractères spéciaux)
    # et a une longueur minimale de 8 caractères.
    pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    if re.match(pattern, password):
        return True
    return False


def hash_password(password):
    '''Hash le password de l'admin'''
    # Encode le mot de passe en bytes
    password_bytes = password.encode('utf-8')
    # Crée un objet sha256
    sha256 = hashlib.sha256()
    # Met à jour l'objet sha256 avec les bytes du mot de passe
    sha256.update(password_bytes)
    # Retourne le hachage en format hexadécimal
    return sha256.hexdigest()


def is_valid_phone_number(phone_number):
    """
    Vérifie si le numéro de téléphone est bien formaté.
    """
    
    # Format attendu: (123) 23456789, 123-23456789, 123 23456789, 12323456789
    # - L'indicatif régional (area code) de 3 chiffres
    # - Le numéro spécifique de 8 chiffres commençant par un chiffre de 2 à 5

    # ^ : début de la chaîne
    # (\\(\\d{3}\\)|\\d{3}) : soit un indicatif régional
    # entre parenthèses (123), soit 3 chiffres 123
    # [-\\s]? : un séparateur optionnel (espace ou tiret)
    # ---------([2-5]\\d{7})
    # [2-5] : le premier chiffre du numéro spécifique doit être
    # compris entre 2 et 5
    # \\d {7} : suivi de 7 chiffres supplémentaires, formant ainsi
    # un total de 8 chiffres pour le numéro spécifique
    # $ : fin de la chaîne

    pattern = r'^(\\(\d{3}\\)|\d{3})[-\s]?([2-5]\d{7})$'
    return re.match(pattern, phone_number) is not None


def is_valid_email(email):
    """
    Vérifie si l'email est bien formaté.
    """
    # ^ : début de la chaîne
    # [a-zA-Z0-9._%+-]+ : une ou plusieurs lettres, chiffres, points,
    # tirets, soulignements, pourcentages, plus ou moins
    # @ : le symbole @
    # [a-zA-Z0-9.-]+ : une ou plusieurs lettres, chiffres, points ou tirets
    # \. : un point
    # [a-zA-Z]{2,} : deux lettres ou plus pour le domaine de niveau supérieur
    # $ : fin de la chaîne
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def display_list_columns(elements):
    """
    Affiche les éléments d'une liste sous des colonnes appropriées.
    """
    # Args:elements (list): La liste des éléments à afficher.
    if not elements:
        print("La liste est vide.")
        return
    # Déterminer le nombre d'éléments
    num_elements = len(elements)
    # Créer la chaîne de formatage dynamique
    format_string = " ".join(["{:<20}"] * num_elements)
    # Formater les éléments
    formatted_string = format_string.format(*elements)
    # Afficher les éléments
    print(formatted_string)


class Person:
    """Classe de récupération des infos d'une personne."""
    def __init__(self):
        self.first_name = ''
        self.last_name = ''
        self.email = ''

    def f_name(self):
        """methode de récupération du prenom d'une personne"""
        self.first_name = is_empty("Entrer votre prénom (x --> quitter):")
        return self.first_name

    def l_name(self):
        """methode de récupération du nom de famille d'une personne"""
        self.last_name = is_empty("Entrer votre nom (x --> quitter):")
        return self.last_name

    def mail(self):
        """methode de récupération de l'email d'une personne"""
        while True:
            self.email = is_empty("Entrer votre adresse mail (x --> quitter):")
            if self.email.lower() == 'x':
                return False
            if is_valid_email(self.email):
                    return self.email
            print('\n', ' '*20, "Votre email n'est pas valide."
                          "Veuillez reessayer.")


def attendre_touche():
    """
    Attend que l'utilisateur appuie sur une touche pour continuer.
    """
    try:
        print('\n', ' '*20, "Appuyez sur ENTER pour continuer...")
        input("\t\t\t\t")
    except KeyboardInterrupt:
        pass  # Gère l'interruption par Ctrl+C


def clear_screen():
    """
    Efface l'écran de la console.
    """
    if platform.startswith('win'):  # Windows
        os.system('cls')
    elif platform.startswith('darwin') or platform.startswith('linux'):
        os.system('clear')
    else:
        # Cas par défaut : tentative de clear pour d'autres systèmes
        os.system('cls' if os.name == 'nt' else 'clear')


def verifier_format_heure_v1(heure):
    """
    Vérifie que l'heure est bien formatée au format HH:MM.

    :param heure: La chaîne de caractères représentant l'heure (e.g., '14:30')
    :return: True si l'heure est bien formatée, False sinon
    """
    try:
        datetime.strptime(heure, '%H:%M')
        return True
    except ValueError:
        return False
    # La méthode strptime est donc très utile pour valider et
    # convertir des chaînes de caractères représentant
    # des dates et des heures en objets datetime utilisables
    # dans des opérations de traitement de dates et d'heures
    # en Python


def verifier_format_heure_v2(heure):
    """
    Vérifie si l'heure est au format HH:MM.

    :param heure: Heure à vérifier (e.g., '10:30')
    :return: True si l'heure est au format correct, False sinon
    """
    pattern = re.compile(r'^([01]\d|2[0-3]):([0-5]\d)$')
    return bool(pattern.match(heure))

    # Exemple d'utilisation
    # print(verifier_format_heure("10:30"))  # True
    # print(verifier_format_heure("25:00"))  # False
    # print(verifier_format_heure("8:00"))   # False
    # print(verifier_format_heure("08:60"))  # False


def verifier_plage_horaire(heure):
    """
    Vérifie que l'heure n'est pas inférieure à 8h du matin ou supérieure à 16h.

    :param heure: Heure à vérifier (e.g., '10:30')
    :return: True si l'heure est dans la plage autorisée, False sinon
    """

    heure_h, minute_m = map(int, heure.split(':'))
    heure_min = 8 * 60
    heure_max = 16 * 60

    heure_total = heure_h * 60 + minute_m
    return heure_min <= heure_total <= heure_max

    # Exemple d'utilisation
    # print(verifier_plage_horaire("07:59"))  # False
    # print(verifier_plage_horaire("08:00"))  # True
    # print(verifier_plage_horaire("12:30"))  # True
    # print(verifier_plage_horaire("16:00"))  # True
    # print(verifier_plage_horaire("16:01"))  # False
    # print(verifier_plage_horaire("25:00"))  # False (mauvais format)


def afficher_entete(column_names):
    '''Détermination de la largeur des colonnes'''
    colonne_width = [len(name) for name in column_names]

    # Création d'une ligne de séparation
    separateur = ('+' +
                  '+'.join('-' * (width + 2) for width in colonne_width) +
                  '+')

    # Affichage de l'entête de la table
    header = '|' + '|'.join(
        f' {name:<{width}} ' for name,
        width in zip(column_names, colonne_width)
        ) + '|'
    print(' '*15, separateur)
    print(' '*15, header)
    print(' '*15, separateur)
    return colonne_width, separateur


def afficher_donnees(data, colonne_width, separateur):
    """Affichage des lignes de la table"""
    for row in data:
        line = ('|' +
                '|'.join(f' {str(value):<{width}} ' for value,
                         width in zip(row, colonne_width)) +
                '|')
        print(' '*15, line)
    print(' ' * 15, separateur)


def afficher_texte_progressivement(texte, delai=0.06):
    """
    Affiche le texte progressivement caractère par caractère.

    :param texte: Le texte à afficher.
    :param delai: Le délai en secondes entre chaque caractère
    (par défaut 0.1 seconde).
    """
    # texte2 = f'{' '*20,}'+ texte
    for caractere in texte:
        print(caractere, end='', flush=True)
        sleep(delai)
    print()
    # Pour passer à la ligne suivante après l'affichage complet du texte
def welcome( bienvenue):
    """
    Affiche le texte progressivement caractère par caractère.

    :param texte: Le texte à afficher.
    :param delai: Le délai en secondes entre chaque caractère
    (par défaut 0.1 seconde).
    """
    print("\n\n")
    print(' ' * 27, "  ____  _   _   ____   _ ")
    print(' ' * 27, " / ___)| | | | / ___) | |")
    print(' ' * 27, "| |    | |_| || |     | |")
    print(' ' * 27, "| |___ |  _  || |___  | |___")
    print(' ' * 27, " \\____)|_| |_| \\____) |_____)")
    print("\n\n")
   
    text = (' ' * 24 +
            "Bienvenue dans le système de gestion\n" +
            ' ' * 20 +
            "des salles de cours de l'université CHCL.")
    texte_bienvenue = ("\n\n" +
                       ' ' * 15 +
        "->Il est recommandé de lancer le programme\n" +
        ' ' * 15 + "->dans un terminal en full screen pour une meilleure\n" +
         ' ' * 15 + "->experience(surtout pour l'affichage des tableaux).")
    Warning_ = ("\n\n\t\t" +
                       ' ' * 20 +
        "ATTENTION!!!\n" +
        ' ' * 12 + "-> Les Id ainsi que les mots de passes sont sensibles a la case..")
    
    print(' ' * 17,'_' * 50, '\n')

    if bienvenue:
        for caractere in text:
            print(caractere, end='', flush=True)
            sleep(0.01)
        
        print()
        attendre_touche()
        for caractere in Warning_:
            print(caractere, end='', flush=True)
            sleep(0.01)
        print()
        attendre_touche()
        for caractere in texte_bienvenue:
            print(caractere, end='', flush=True)
            sleep(0.01)
        print()    
    
    bienvenue = False
    # Pour passer à la ligne suivante après l'affichage complet du texte
