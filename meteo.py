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

# requete API pour récupérer les données météo avec coordonnées GPS

def get_meteo_gps(lat, lon):
    api_key = "657d085c1641acc8912db3f95ecd21b3"
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=fr&appid={api_key}"
    
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




# Afficher 
def afficher_meteo(ville):
    data = get_meteo(ville)

    if data:
        informationGenerale = data["main"]["temp"]
        description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidite = data["main"]["humidity"]
        vitesseVent = data["wind"]["speed"]
        directionVent = data["wind"]["deg"]
    
        print(f"\nInformation météo pour {ville}:")
        print(f"Description : {informationGenerale}")
        print(f"Température : {temperature} °C")
        print(f"Humidité : {humidite} %")
        print(f"Vitesse du vent : {vitesseVent} km/h")
        print(f"Direction du vent : {directionVent}\n")
    else:
        print(f"Les données météo pour {ville} ne sont pas disponibles. Veuillez vérifier le nom de la ville.")

# Afficher la météo avec les coordonnées GPS

def afficher_meteo_gps(lat, lon):
    data = get_meteo_gps(lat, lon)
    
    if data:
        informationGenerale = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidite = data["main"]["humidity"]
        vitesseVent = data["wind"]["speed"]
        directionVent = data["wind"]["deg"]
        nomVille = data["name"]
        
        print(f"\nInformation météo pour la position ({lat}, {lon}):")
        print(f"Ville : {nomVille}")
        print(f"Description : {informationGenerale}")
        print(f"Température : {temperature} °C")
        print(f"Humidité : {humidite} %")
        print(f"Vitesse du vent : {vitesseVent} km/h")
        print(f"Direction du vent : {directionVent}\n")
    else:
        print(f"Les données météo pour la position ({lat}, {lon}) ne sont pas disponibles. Veuillez vérifier les coordonnées GPS.")

def cli_interactif():
    ville_defaut = "Avignon"
    print(f"Bienvenue dans l'application météo CLI (ville par défaut : {ville_defaut}).")
    
    while True:
        choix = input("Entrez '1' pour rechercher par nom de ville, '2' pour rechercher par coordonnées GPS, ou 'q' pour quitter : ")
        
        if choix == 'q':
            print("Au revoir !")
            break
        
        if choix == '1':
            ville = input("Entrez le nom de la ville (ou appuyez sur Entrée pour utiliser la ville par défaut) : ")
            
            if ville.strip() == "":
                ville = ville_defaut
            
            afficher_meteo(ville)
        
        elif choix == '2':
            lat = input("Entrez la latitude : ")
            lon = input("Entrez la longitude : ")
            
            afficher_meteo_gps(lat, lon)
        
        else:
            print("Choix invalide. Veuillez réessayer.")


if __name__ == "__main__":
    cli_interactif()
