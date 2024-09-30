import requests
import sys
import datetime

# Fonction pour obtenir la météo actuelle
def get_meteo_actuelle(ville=None):
    api_key = "657d085c1641acc8912db3f95ecd21b3"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ville}&units=metric&lang=fr&appid={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data.get('cod') != 200:
            print(f"Erreur : {data.get('message', 'Données météo non disponibles')}.")
            return None
        
        return data
    except requests.exceptions.RequestException:
        print("Erreur : Impossible de récupérer les données météo.")
        return None

# Fonction pour obtenir les prévisions à 5 jours
def get_forecast(ville=None):
    api_key = "657d085c1641acc8912db3f95ecd21b3"
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={ville}&units=metric&lang=fr&appid={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data.get('cod') != "200":
            print(f"Erreur : {data.get('message', 'Données météo non disponibles')}.")
            return None
        
        # Créer un tableau avec les prévisions
        forecast_list = []
        for forecast in data['list']:
            forecast_info = {
                'date': forecast['dt_txt'],
                'temperature': forecast['main']['temp'],
                'humidity': forecast['main']['humidity'],
                'wind_speed': forecast['wind']['speed'] * 3.6,  # conversion en km/h
                'description': forecast['weather'][0]['description']
            }
            forecast_list.append(forecast_info)
        
        return forecast_list
    except requests.exceptions.RequestException:
        print("Erreur : Impossible de récupérer les données météo.")
        return None

# Fonction pour obtenir la météo à une date spécifique (à 12h)
def get_meteo_by_date(ville=None, date_str=None):
    data = get_forecast(ville)
    if not data:
        return "Données indisponibles"

    # Convertir la date fournie en objet datetime
    try:
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return "Format de date invalide. Utilisez 'AAAA-MM-JJ'."

    # Chercher la prévision à 12h pour cette date
    for forecast in data:
        forecast_date = datetime.datetime.strptime(forecast['date'], "%Y-%m-%d %H:%M:%S")
        if forecast_date.date() == date_obj and forecast_date.hour == 12:
            return [forecast]  # Renvoie la prévision correspondante à 12h
    
    return "Aucune prévision trouvée pour cette date à 12h."

# Fonction pour afficher la météo actuelle ou à une date spécifique
def afficher_meteo(ville, date_str=None):
    if date_str:
        forecast = get_meteo_by_date(ville, date_str)
        if isinstance(forecast, dict):
            print(f"\nPrévisions météo pour {ville} le {date_str} à 12h :")
            print(f"Description : {forecast['weather'][0]['description']}")
            print(f"Température : {forecast['main']['temp']} °C")
            print(f"Humidité : {forecast['main']['humidity']} %")
            print(f"Vitesse du vent : {forecast['wind']['speed'] * 3.6} km/h")
        else:
            print(forecast)
    else:
        data = get_meteo_actuelle(ville)
        if data:
            print(f"\nMétéo actuelle pour {ville}:")
            print(f"Description : {data['weather'][0]['description']}")
            print(f"Température : {data['main']['temp']} °C")
            print(f"Humidité : {data['main']['humidity']} %")
            print(f"Vitesse du vent : {data['wind']['speed'] * 3.6} km/h")
        else:
            print(f"Les données météo pour {ville} ne sont pas disponibles.")

# Fonction principale pour gérer les arguments
def main():
    ville_defaut = "Avignon"
    
    # Récupérer les arguments passés en ligne de commande
    args = sys.argv[1:]
    
    ville = ville_defaut
    date_str = None
    
    if '-d' in args:
        index = args.index('-d')
        if index + 1 < len(args):
            date_str = args[index + 1]
        else:
            print("Erreur : Veuillez fournir une date après l'option '-d'.")
            return
    
    # Si une ville est donnée comme argument (avant -d ou après)
    if len(args) > 0 and args[0] != '-d':
        ville = args[0]
    
    # Afficher la météo (actuelle ou prévisions selon le cas)
    afficher_meteo(ville, date_str)

if __name__ == "__main__":
    main()
