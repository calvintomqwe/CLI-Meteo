import requests
import sys
import json
import csv
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QFont
from PyQt5.QtCore import Qt, QTimer

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
        return None




# Afficher 
def afficher_meteo_A(ville):

    data = get_meteo(ville)

    if data:
        temperature = data["main"]["temp"]
        humidite = data["main"]["humidity"]
        vitesseVent = data["wind"]["speed"]
        #directionVent = data["wind"]["deg"]


        #retourner un tableau avec les informations météo
        meteo = [ville, "aujourd'hui", temperature, humidite, vitesseVent]
        return meteo
    
    else:
        return "Les données météo pour " + ville + " ne sont pas disponibles. Veuillez vérifier le nom de la ville."

# Afficher la météo avec les coordonnées GPS

def afficher_meteo_gps_A(lat, lon):
    data = get_meteo_gps(lat, lon)
    
    if data:
        temperature = data["main"]["temp"]
        humidite = data["main"]["humidity"]
        vitesseVent = data["wind"]["speed"]
        directionVent = data["wind"]["deg"]
        nomVille = data["name"]

        #retourner un tableau avec les informations météo
        meteo = [nomVille, "aujourd'hui", temperature, humidite, vitesseVent, directionVent]
        return meteo

    else:
        return "Les données météo pour la position (" + lat + "," + lon + ") ne sont pas disponibles. Veuillez vérifier les coordonnées GPS."
    
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


# Afficher et enregistrer le résultat sous forme CSV
def afficher_meteo_csv(ville, options):   
    file_name = f"meteo.csv"
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Créer dynamiquement les en-têtes en fonction des options
        headers = ["Ville", "Date"]
        if param[0]:
            headers.append("Température (°C)")
        if param[1]:
            headers.append("Humidité (%)")
        if param[2]:
            headers.append("Vitesse du vent (km/h)")
        
        # Ecrire les en-têtes
        writer.writerow(headers)

        for data in ville:
            try:
                # Construire la ligne de données en fonction des options choisies
                row = [data[0], data[1]]  # Ville, Date
                if param[0]:
                    row.append(data[2])  # Température
                if param[1]:
                    row.append(data[3])  # Humidité
                if param[2]:
                    row.append(data[4])  # Vitesse du vent
                
                # Ecrire les données
                writer.writerow(row)
            
            except IndexError:
                print(f"Erreur : les données pour {data[0]} ne sont pas complètes.")

def afficher_avignon_en_gros():
    print("""
     A     V     V  I  GGGGG  N   N  OOO   N   N
    A A     V   V   I  G      NN  N O   O  NN  N
   AAAAA     V V    I  G  GG  N N N O   O  N N N
  A     A     V     I  G   G  N  NN O   O  N  NN
 A       A    V     I   GGGG  N   N  OOO   N   N
    """)


# Fonction pour obtenir les prévisions à 5 jours
def get_forecast(ville=None):
    api_key = "657d085c1641acc8912db3f95ecd21b3"
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={ville}&units=metric&lang=fr&appid={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data.get('cod') != "200":
            return "Erreur : {data.get('message', 'Données météo non disponibles')}."
        
        # Créer un tableau avec les prévisions
        forecast_list = []
        for forecast in data['list']:
            forecast_info = {
                'name': ville,
                'date': forecast['dt_txt'],
                'temperature': forecast['main']['temp'],
                'humidity': forecast['main']['humidity'],
                'wind_speed': forecast['wind']['speed'] * 3.6,  # conversion en km/h
                'description': forecast['weather'][0]['description']
            }
            forecast_list.append(forecast_info)
        
        return forecast_list
    except requests.exceptions.RequestException:
        return "Erreur : Impossible de récupérer les données météo."

# Fonction pour obtenir la météo à une date spécifique (à 12h)
def get_meteo_by_date(ville=None, date_str=None):
    data = get_forecast(ville)
    if not data:
        return "Données indisponibles"

    # Convertir la date fournie en objet datetime
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return "Format de date invalide. Utilisez 'AAAA-MM-JJ'."

    # Chercher la prévision à 12h pour cette date
    for forecast in data:
        forecast_date = datetime.strptime(forecast['date'], "%Y-%m-%d %H:%M:%S")
        if forecast_date.date() == date_obj and forecast_date.hour == 12:
            return [forecast]  # Renvoie la prévision correspondante à 12h
    
    return "Aucune prévision trouvée pour "+ ville + " le " + date_str

# Fonction pour obtenir les prévisions à 5 jours
def get_forecast_coord(lat=None,long=None):
    api_key = "657d085c1641acc8912db3f95ecd21b3"
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={long}&units=metric&lang=fr&appid={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data.get('cod') != "200":
            return "Erreur : {data.get('message', 'Données météo non disponibles')}."
        
        # Créer un tableau avec les prévisions
        forecast_list = []
        for forecast in data['list']:
            forecast_info = {
                'name': lat+":"+long,
                'date': forecast['dt_txt'],
                'temperature': forecast['main']['temp'],
                'humidity': forecast['main']['humidity'],
                'wind_speed': forecast['wind']['speed'] * 3.6,  # conversion en km/h
                'description': forecast['weather'][0]['description']
            }
            forecast_list.append(forecast_info)
        
        return forecast_list
    except requests.exceptions.RequestException:
        return "Erreur : Impossible de récupérer les données météo."

# Fonction pour obtenir la météo à une date spécifique (à 12h)
def get_meteo_by_coord_by_date(lat=None,long=None, date_str=None):
    data = get_forecast_coord(lat,long)
    if not data:
        return "Données indisponibles"

    # Convertir la date fournie en objet datetime
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return "Format de date invalide. Utilisez 'AAAA-MM-JJ'."

    # Chercher la prévision à 12h pour cette date
    for forecast in data:
        forecast_date = datetime.strptime(forecast['date'], "%Y-%m-%d %H:%M:%S")
        if forecast_date.date() == date_obj and forecast_date.hour == 12:
            return [forecast]  # Renvoie la prévision correspondante à 12h
    
    return "Aucune prévision trouvée pour "+ lat+":"+long + " le " + date_str

# Fonction pour afficher la météo actuelle ou à une date spécifique
def transfo_meteo_si_date(date, forecast):
    if isinstance(forecast, str):
        return forecast

    nom_ville = forecast[0]['name']
    #description = forecast[0]['description']
    temperature = forecast[0]['temperature']
    humidite = forecast[0]['humidity']
    vitesse_vent = forecast[0]['wind_speed']  # vitesse en km/h
    #direction_vent = None  # Les prévisions ne contiennent pas de direction de vent dans ce cas

    # Retourner un tableau similaire à celui de 'afficher_meteo_A'
    meteo = [nom_ville, date, temperature, humidite, vitesse_vent]
    
    return meteo
        
def liste_dates(date_debut, date_fin):
    debut = datetime.strptime(date_debut, "%Y-%m-%d")
    fin = datetime.strptime(date_fin, "%Y-%m-%d")

    liste_jours = []

    delta = timedelta(days=1)
    while debut <= fin:
        liste_jours.append(debut.strftime("%Y-%m-%d"))
        debut += delta

    return liste_jours

def prochaines_dates():
    """Retourne les dates d'aujourd'hui, de demain et d'après-demain au format AAAA-MM-JJ."""
    aujourd_hui = datetime.today()
    demain = aujourd_hui + timedelta(days=1)
    apres_demain = aujourd_hui + timedelta(days=2)
    
    return [
        aujourd_hui.strftime("%Y-%m-%d"),
        demain.strftime("%Y-%m-%d"),
        apres_demain.strftime("%Y-%m-%d")
    ]

def traitement(villes_tableau):
    returnTab = []
    for ville_data in villes_tableau:
        if(ville_data[4] == 'a'):
            nom_ville = ville_data[0]
            liste = prochaines_dates()
            for date in liste:
                returnTab.append(transfo_meteo_si_date(date, get_meteo_by_date(nom_ville, date)))
        elif(ville_data[4] == 'v'):
            nom_ville = ville_data[0]
            dates = ville_data[1:4]
            if all(date is None for date in dates):
                returnTab.append(afficher_meteo_A(nom_ville))
            elif(dates[0] is not None):
                returnTab.append(transfo_meteo_si_date(dates[0], get_meteo_by_date(nom_ville, dates[0])))
            elif(dates[1] is not None and dates[2] is not None):
                liste = liste_dates(dates[1],dates[2])
                for date in liste:
                    returnTab.append(transfo_meteo_si_date(date, get_meteo_by_date(nom_ville, date)))
            else:
                print("error")
        elif(ville_data[4] == 'c'):
            coord = ville_data[0].split(':')
            if len(coord) == 2 and coord[0] and coord[1]:
                nom_ville = ville_data[0]
                dates = ville_data[1:4]
                if all(date is None for date in dates):
                    returnTab.append(afficher_meteo_gps_A(coord[0], coord[1]))
                elif(dates[0] is not None):
                    returnTab.append(transfo_meteo_si_date(dates[0], get_meteo_by_coord_by_date(coord[0], coord[1], dates[0])))
                elif(dates[1] is not None and dates[2] is not None):
                    liste = liste_dates(dates[1],dates[2])
                    for date in liste:
                        returnTab.append(transfo_meteo_si_date(date, get_meteo_by_coord_by_date(coord[0], coord[1], date)))
                else:
                    print("error")
            else:
                print(ville_data[0] + " n'est pas une coordonnée valide essayer le format lat:long")
        else:
            print("Choix invalide. Veuillez entrer 'villes' ou 'coordonnées'.")
    return returnTab

def afficher_aide():
    try:
        with open('help_meteo_cli.txt', 'r', encoding='utf-8') as file:
            aide_contenu = file.read()
            print(aide_contenu)
    except FileNotFoundError:
        print("Erreur : Le fichier d'aide help est introuvable.")

# Fonction principale pour gérer les argument

def traiter_arguments():
    args = sys.argv[1:]
    villes = []
    #       [default,temp,hum,wind]
    param = [False,False,False,False]
    ifcsv = False
    i = 0
    if len(args) == 0:
        villes.append([lire_ville_defaut(),None,None,None,'v'])
    while i < len(args):
        if args[i] == "-csv":
            ifcsv = True
        if args[i] == '-temp':
            if param[0] == False: param[0] = True
            param[1] = True
        if args[i] == '-hum':
            if param[0] == False: param[0] = True
            param[2] = True
        if args[i] == '-wind':
            if param[0] == False: param[0] = True
            param[3] = True
        if args[i] == '-default':
            changer_ville_defaut(args[i + 1])
        if args[i] == '-help':
            afficher_aide()
        if args[i] == '-app':
            tab = []
            tab.append([lire_ville_defaut(),None,None,None,'a'])
            aze = traitement(tab)
        if args[i] == '-v':
            ville_info = [None, None, None, None, 'v']
            ville_info[0] = args[i + 1]
            i += 2

            if i < len(args) and args[i] == '-d':
                ville_info[1] = args[i + 1]
                i += 2

            elif i < len(args) and args[i] == '-p':
                ville_info[2] = args[i + 1]
                ville_info[3] = args[i + 2]
                i += 3

            villes.append(ville_info)
        elif args[i] == "-c":
            ville_info = [None, None, None, None, 'c']
            ville_info[0] = args[i + 1]
            i += 2

            if i < len(args) and args[i] == '-d':
                ville_info[1] = args[i + 1]
                i += 2

            elif i < len(args) and args[i] == '-p':
                ville_info[2] = args[i + 1]
                ville_info[3] = args[i + 2]
                i += 3

            villes.append(ville_info)
        else:
            i += 1

    return villes, param, ifcsv, aze


class WeatherApp():
    def __init__(self, weather_data, params):
        """
        weather_data: tableau contenant les données météo
        params: tableau contenant les préférences d'affichage
        """
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        # Variables initiales
        self.weather_data = weather_data
        self.params = params
        self.current_temp = f"{weather_data[0][2]}°"
        
        # Créer une icône de température
        self.temp_icon = QSystemTrayIcon(self.generate_temp_icon(self.current_temp), self.app)

        # Ajouter un menu contextuel pour quitter
        self.menu = QMenu()
        quit_action = QAction("Quitter", self.app)
        quit_action.triggered.connect(self.exit_app)
        self.menu.addAction(quit_action)
        self.temp_icon.setContextMenu(self.menu)

        # Rendre l'icône visible
        self.temp_icon.setVisible(True)

        # Créer la fenêtre flottante pour les prévisions
        self.create_forecast_window()

        # Connecter un clic sur l'icône pour ouvrir la fenêtre des prévisions
        self.temp_icon.activated.connect(self.on_icon_clicked)

    def generate_temp_icon(self, temperature):
        """Créer une icône avec la température en texte."""
        temp_pixmap = QPixmap(64, 64)  # Taille fixée de 64x64 pixels
        temp_pixmap.fill(Qt.transparent)

        painter = QPainter(temp_pixmap)
        painter.setFont(QFont("Arial", 18, QFont.Bold))
        painter.setPen(Qt.black)
        painter.drawText(10, 40, temperature)
        painter.end()

        return QIcon(temp_pixmap)

    def create_forecast_window(self):
        """Créer une fenêtre flottante pour afficher les prévisions météo."""
        self.forecast_window = QWidget()
        self.forecast_window.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.forecast_window.setStyleSheet("background-color: white; border: 1px solid gray;")
        self.forecast_window.setFixedSize(300, 200)

        layout = QVBoxLayout()

        # Remplir les prévisions avec les données du tableau
        for info in self.weather_data:
            if isinstance(info, str):
                label = QLabel(info)
            else:
                if info[1] == "aujourd'hui":
                    label = QLabel(f"Météo pour {info[0]} aujourd'hui:")
                else:
                    label = QLabel(f"Météo pour {info[0]} le {info[1]}:")

                details = []
                if self.params[0] == False or self.params[1] == True:
                    details.append(f"Température : {info[2]} °C")
                if self.params[0] == False or self.params[2] == True:
                    details.append(f"Humidité : {info[3]} %")
                if self.params[0] == False or self.params[3] == True:
                    details.append(f"Vent : {info[4]} m/h")
                label.setText(label.text() + "\n" + "\n".join(details))

            layout.addWidget(label)

        self.forecast_window.setLayout(layout)

    def on_icon_clicked(self, reason):
        """Afficher les prévisions météo lorsque l'icône est cliquée."""
        if reason == QSystemTrayIcon.Trigger:  # Clic gauche
            self.show_forecast_window()

    def show_forecast_window(self):
        """Afficher ou cacher la fenêtre des prévisions météo."""
        if self.forecast_window.isVisible():
            self.forecast_window.hide()
        else:
            screen_geometry = QApplication.desktop().screenGeometry()
            taskbar_height = 50
            self.forecast_window.move(screen_geometry.width() - self.forecast_window.width(),
                                      screen_geometry.height() - self.forecast_window.height() - taskbar_height - 10)
            self.forecast_window.show()

    def exit_app(self):
        """Quitter l'application proprement."""
        self.forecast_window.close()
        self.temp_icon.hide()
        sys.exit()

    def run(self):
        """Lancer l'application."""
        sys.exit(self.app.exec_())



if __name__ == "__main__":
    villes, param, ifcsv, aze = traiter_arguments()
    tab = traitement(villes)
    if ifcsv:
        afficher_meteo_csv(tab,param)
    else:
        for info in tab:
            if isinstance(info, str):
                print(info)
            else:
                if(info[1] == "aujourd'hui"):
                    print(f"\nMétéo actuelle pour {info[0]} aujourd'hui:")
                else:
                    print(f"\nMétéo actuelle pour {info[0]} le {info[1]}:")
                if(param[0] == False or param[1] == True):
                    print(f"Température : {info[2]} °C")
                if(param[0] == False or param[2] == True):
                    print(f"Humidité : {info[3]} %")
                if(param[0] == False or param[3] == True):
                    print(f"Vitesse du vent : {info[4]} m/h")
    if aze != 0:
        weather_app = WeatherApp(aze,[True, True, True, True])
        weather_app.run()
