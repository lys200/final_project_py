import re

def verifier_format_heure(heure):
    """
    Vérifie si l'heure est au format HH:MM.

    :param heure: Heure à vérifier (e.g., '10:30')
    :return: True si l'heure est au format correct, False sinon
    """
    pattern = re.compile(r'^([01]\d|2[0-3]):([0-5]\d)$')
    return bool(pattern.match(heure))

def convertir_en_minutes(heure):
    """
    Convertit une heure au format HH:MM en minutes totales depuis minuit.

    :param heure: Heure au format HH:MM
    :return: Minutes totales depuis minuit
    """
    heure_h, minute_m = map(int, heure.split(':'))
    return heure_h * 60 + minute_m

def convertir_en_hhmm(minutes):
    """
    Convertit des minutes totales en format HH:MM.

    :param minutes: Minutes totales depuis minuit
    :return: Chaîne représentant la durée en format HH:MM
    """
    heures = minutes // 60
    minutes = minutes % 60
    return f"{heures:02d}:{minutes:02d}"

def additionner_heures(heure1, heure2):
    """
    Additionne deux heures au format HH:MM.

    :param heure1: Première heure au format HH:MM
    :param heure2: Deuxième heure au format HH:MM
    :return: Somme des deux heures au format HH:MM
    """
    if not verifier_format_heure(heure1) or not verifier_format_heure(heure2):
        raise ValueError("L'une des heures n'est pas au format HH:MM")

    minutes_totales_heure1 = convertir_en_minutes(heure1)
    minutes_totales_heure2 = convertir_en_minutes(heure2)

    minutes_totales = minutes_totales_heure1 + minutes_totales_heure2
    return convertir_en_hhmm(minutes_totales)

# Exemples d'utilisation
print(additionner_heures("01:30", "02:45"))  # 04:15
print(additionner_heures("10:15", "05:30"))  # 15:45
print(additionner_heures("23:15", "02:30"))  # 25:45 (1 jour + 01:45)
print(additionner_heures("00:00", "00:00"))  # 00:00
