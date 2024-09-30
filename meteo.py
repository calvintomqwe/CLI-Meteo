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
    
# fonction pour changer la ville par default en stockant dans un fichier

def changer_ville_defaut(ville):
    with open("ville_defaut.txt", "w") as f:
        f.write(ville)
    
# fonction pour lire la ville par default dans le fichier

def lire_ville_defaut():
    try:
        with open("ville_defaut.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return None


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
            
            #tableau avec les informations météo et afficher le tableau
            meteo = afficher_meteo(ville)
            if meteo:
                print(f"\nMétéo à {meteo[0]} :")
                print(f"Description : {meteo[1]}")
                print(f"Température : {meteo[2]} °C")
                print(f"Hygrométrie : {meteo[3]} %")
                print(f"Vitesse du vent : {meteo[4]} m/s")
                print(f"Direction du vent : {meteo[5]} °\n")
            else:
                print("Les données météo ne sont pas disponibles.")
            
        
        elif choix == '2':
            lat = input("Entrez la latitude : ")
            lon = input("Entrez la longitude : ")
            
            #tableau avec les informations météo et afficher le tableau
            meteo = afficher_meteo_gps(lat, lon)
            if meteo:
                print(f"\nMétéo à {meteo[0]} :")
                print(f"Description : {meteo[1]}")
                print(f"Température : {meteo[2]} °C")
                print(f"Hygrométrie : {meteo[3]} %")
                print(f"Vitesse du vent : {meteo[4]} m/s")
                print(f"Direction du vent : {meteo[5]} °\n")
            else:
                print("Les données météo ne sont pas disponibles.")
        
        else:
            print("Choix invalide. Veuillez réessayer.")


if __name__ == "__main__":
    cli_interactif()
