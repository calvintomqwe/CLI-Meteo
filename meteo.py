import requests
import json

# requête API pour récupérer les données météo
def get_meteo(ville=None):
    api_key = "657d085c1641acc8912db3f95ecd21b3"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ville}&units=metric&lang=fr&appid={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # vérifie si la requête a échoué
        data = response.json()
        
        if data.get('cod') != 200:
            print(f"Erreur : {data.get('message', 'Données météo non disponibles')}.")
            return None
            
        return data
    except requests.exceptions.RequestException:
        print("Erreur : Impossible de récupérer les données météo.")
        return None


# Fonctions pour récupérer les données météo

# Récupérer la température
def get_temperature(ville=None):
    data = get_meteo(ville)
    if data:
        return data["main"]["temp"]
    return "Données indisponibles"

# Récupérer l'humidité
def get_humidity(ville=None):
    data = get_meteo(ville)
    if data:
        return data["main"]["humidity"]
    return "Données indisponibles"

# Récupérer la vitesse du vent
def get_wind_speed(ville=None):
    data = get_meteo(ville)
    if data:
        wind_speed = data["wind"]["speed"]
        return wind_speed * 3.6  # convertir de m/s à km/h
    return "Données indisponibles"

# Récupérer la direction du vent
def get_wind_direction(ville=None):
    data = get_meteo(ville)
    if data:
        degrees = data["wind"]["deg"]
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N']
        index = round(degrees / 45) # arrondir à la direction la plus proche
        return directions[index]
    return "Données indisponibles"

# Récupérer la description 
def get_weather_description(ville=None):
    data = get_meteo(ville)
    if data:
        return data["weather"][0]["description"]
    return "Données indisponibles"

# Afficher 
def afficher_meteo(ville):
    data = get_meteo(ville)
    
    if data:
        print(f"\nInformation météo pour {ville}:")
        print(f"Description : {get_weather_description(ville)}")
        print(f"Température : {get_temperature(ville)} °C")
        print(f"Humidité : {get_humidity(ville)} %")
        print(f"Vitesse du vent : {get_wind_speed(ville)} km/h")
        print(f"Direction du vent : {get_wind_direction(ville)}\n")
    else:
        print(f"Les données météo pour {ville} ne sont pas disponibles. Veuillez vérifier le nom de la ville.")


def cli_interactif():
    ville_defaut = "Avignon"
    print(f"Bienvenue dans l'application météo CLI (ville par défaut : {ville_defaut}).")
    
    while True:
        ville = input("Entrez le nom de la ville (ou appuyez sur Entrée pour utiliser la ville par défaut, ou tapez 'q' pour quitter) : ")
        
        if ville.lower() == 'q':
            print("Au revoir !")
            break
        
        if ville.strip() == "":
            ville = ville_defaut
        
        afficher_meteo(ville)


if __name__ == "__main__":
    cli_interactif()
