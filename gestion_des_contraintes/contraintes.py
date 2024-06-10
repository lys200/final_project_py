"""
    Ce module contient les differents test de contraintes
"""
from datetime import datetime
import re
import hashlib

def is_empty(input_message):
    """Verifie que le champs rempli par le user n'est pas vide."""
    while True:
        user_input = input(input_message).strip()
        if user_input:
            return user_input
        else:
            print("L'entrée ne peut pas être vide ou ne contenir que des espaces. Veuillez réessayer.")

def is_integer(number):
    return isinstance(number, int)

def is_valid_password(password):
    """Verifie si le mot de passe a au moins une majuscule, un chiffre et un caractere special. """
    #(?=.*[A-Z]):  vérifie qu'il y a au moins une lettre majuscule dans la chaîne.
    #(?=.*\d): vérifie qu'il y a au moins un chiffre dans la chaîne.
    #(?=.*[@$!%*?&]):  vérifie qu'il y a au moins un des caractères spéciaux spécifiés dans la chaîne.
    #[A-Za-z\d@$!%*?&]{8,}: Cela assure que le mot de passe est composé uniquement des caractères spécifiés (lettres, chiffres, caractères spéciaux) 
    #et a une longueur minimale de 8 caractères.
    pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    if re.match(pattern, password):
        return True
    else:
        return False
def is_valid_number(number):
    pattern = r'(?.*\d)'
def hash_password(password):
    # Encode le mot de passe en bytes
    password_bytes = password.encode('utf-8')
    print(password_bytes)
    # Crée un objet sha256
    sha256 = hashlib.sha256()
    # Met à jour l'objet sha256 avec les bytes du mot de passe
    sha256.update(password_bytes)
    # Retourne le hachage en format hexadécimal
    print(sha256.hexdigest())
    return sha256.hexdigest()


def get_current_datetime():
    # Obtenir la date et l'heure actuelles
    now = datetime.now()
    # Formater la date et l'heure au format désiré
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_now

import re

def is_valid_phone_number(phone_number):
    """
    Vérifie si le numéro de téléphone est bien formaté.
    """
    '''
    Format attendu: (123) 23456789, 123-23456789, 123 23456789, 12323456789
    - L'indicatif régional (area code) de 3 chiffres
    - Le numéro spécifique de 8 chiffres commençant par un chiffre de 2 à 5

    ^ : début de la chaîne
    (\(\d{3}\)|\d{3}) : soit un indicatif régional entre parenthèses (123), soit 3 chiffres 123
    [-\s]? : un séparateur optionnel (espace ou tiret)
    ---------([2-5]\d{7}) 
    [2-5] : le premier chiffre du numéro spécifique doit être compris entre 2 et 5
    \d{7} : suivi de 7 chiffres supplémentaires, formant ainsi un total de 8 chiffres pour le numéro spécifique
    $ : fin de la chaîne
    '''
    pattern = r'^(\(\d{3}\)|\d{3})[-\s]?([2-5]\d{7})$'
    return re.match(pattern, phone_number) is not None

def is_valid_email(email):
    """
    Vérifie si l'email est bien formaté.
    """
    # ^ : début de la chaîne
    # [a-zA-Z0-9._%+-]+ : une ou plusieurs lettres, chiffres, points, tirets, soulignements, pourcentages, plus ou moins
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