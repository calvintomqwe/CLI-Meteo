import requests
import sys
import datetime


# requête API pour récupérer les données météo
def get_meteo(ville=None):
    api_key = "657d085c1641acc8912db3f95ecd21b3"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ville}&units=metric&lang=fr&appid={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # vérifie si la requête a échoué
        data = response.json()

        if data.get('cod') != 200:
            print(
                f"Erreur : {data.get('message', 'Données météo non disponibles')}."
            )
            return None

        return data
    except requests.exceptions.RequestException:
        print("Erreur : Impossible de récupérer les données météo.")
        return None

# requete API pour récupérer les données météo avec coordonnées GPS


def get_meteo_gps(lat, lon):
    api_key = "657d085c1641acc8912db3f95ecd21b3"
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=fr&appid={api_key}"
    
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




# Afficher 
def afficher_meteo_A(ville):

    data = get_meteo(ville)

    if data:
        informationGenerale = data["main"]["temp"]
        description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidite = data["main"]["humidity"]
        vitesseVent = data["wind"]["speed"]
        directionVent = data["wind"]["deg"]


        #retourner un tableau avec les informations météo
        meteo = [ville, informationGenerale, temperature, humidite, vitesseVent, directionVent]
        return meteo
    
    else:
        print(f"Les données météo pour {ville} ne sont pas disponibles. Veuillez vérifier le nom de la ville.")
        return None


# Afficher la météo avec les coordonnées GPS

def afficher_meteo_gps_A(lat, lon):
    data = get_meteo_gps(lat, lon)
    
    if data:
        informationGenerale = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidite = data["main"]["humidity"]
        vitesseVent = data["wind"]["speed"]
        directionVent = data["wind"]["deg"]
        nomVille = data["name"]

        #retourner un tableau avec les informations météo
        meteo = [nomVille, informationGenerale, temperature, humidite, vitesseVent, directionVent]
        return meteo

    else:
        print(f"Les données météo pour la position ({lat}, {lon}) ne sont pas disponibles. Veuillez vérifier les coordonnées GPS.")
        return None



def afficher_meteo_date(ville, date):
    print(f"Affichage des données météo pour {ville} à la date {date}")





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
def afficher_meteo_si_date(ville, date_str=None):
    if date_str:
        forecast = get_meteo_by_date(ville, date_str)
        if isinstance(forecast, dict) and len(forecast)>0:
            print(f"\nPrévisions météo pour {ville} le {date_str} à 12h :")
            for element in forecast:
                print(f"Description : {forecast['weather'][0]['description']}")
                print(f"Température : {element['temperature']} °C")
                print(f"Humidité : {forecast['main']['humidity']} %")
                print(f"Vitesse du vent : {forecast['wind']['speed'] * 3.6} km/h")
        else:
            print(forecast)
    else:
        data = get_meteo(ville)
        if data:
            print(f"\nMétéo actuelle pour {ville}:")
            print(f"Description : {data['weather'][0]['description']}")
            print(f"Température : {data['main']['temp']} °C")
            print(f"Humidité : {data['main']['humidity']} %")
            print(f"Vitesse du vent : {data['wind']['speed'] * 3.6} km/h")
        else:
            print(f"Les données météo pour {ville} ne sont pas disponibles.")
def afficher_aide():
    try:
        with open('help_meteo_cli.txt', 'r', encoding='utf-8') as file:
            aide_contenu = file.read()
            print(aide_contenu)
    except FileNotFoundError:
        print("Erreur : Le fichier d'aide help est introuvable.")

# Fonction principale pour gérer les arguments
def main():
    ville_defaut = "Avignon"
    if '-help' in sys.argv:  # Si l'utilisateur passe l'option -aide
        afficher_aide()
        sys.exit()
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
    afficher_meteo_si_date(ville, date_str)

if __name__ == "__main__":
    main()
