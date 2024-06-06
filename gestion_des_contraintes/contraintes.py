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
    #(?=.*[A-Z]): Cette assertion vérifie qu'il y a au moins une lettre majuscule dans la chaîne.
    #(?=.*\d): Cette assertion vérifie qu'il y a au moins un chiffre dans la chaîne.
    #(?=.*[@$!%*?&]): Cette assertion vérifie qu'il y a au moins un des caractères spéciaux spécifiés dans la chaîne.
    #[A-Za-z\d@$!%*?&]{8,}: Cela assure que le mot de passe est composé uniquement des caractères spécifiés (lettres, chiffres, caractères spéciaux) 
    #et a une longueur minimale de 8 caractères.
    pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    if re.match(pattern, password):
        return True
    else:
        return False
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



