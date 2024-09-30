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



def main():

    choix = input(
        "Voulez-vous entrer des noms de villes ou des coordonnées GPS ? (villes/coordonnées) : "
    ).strip().lower()

    if choix == "villes":
        # Entrée de tableau de villes avec potentiellement des dates
        villes_tableau = [
            ["Montcuq", None, None, None],
            ["Lyon", "2023-09-20", None, None],
            ["Marseille", "2023-09-15", "2023-09-16", None]
        ]

        for ville_data in villes_tableau:
            nom_ville = ville_data[0]
            dates = ville_data[1:4]

            if all(date is None for date in dates):  # Si toutes les dates sont None, appeler afficher_meteo
                afficher_meteo(nom_ville)
            else:  # Sinon, appeler afficher_meteo_date pour les dates non nulles
                for date in dates:
                    if date is not None:
                        afficher_meteo_date(nom_ville, date)

    elif choix == "coordonnées":
        coords_input = input(
            "Entrez les coordonnées GPS (lat,lon), séparées par des virgules : "
        )
        coords = [
            tuple(map(float,
                      coord.strip().split(',')))
            for coord in coords_input.split(',')
        ] if coords_input else []

        for lat, lon in coords:
            afficher_meteo_gps(lat, lon)

    else:
        print("Choix invalide. Veuillez entrer 'villes' ou 'coordonnées'.")




if __name__ == "__main__":
    main()
