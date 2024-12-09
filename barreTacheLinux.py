import requests
import gi
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3, Gtk, GLib

def get_forecast(ville=None):
    api_key = "657d085c1641acc8912db3f95ecd21b3"
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={ville}&units=metric&lang=fr&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get('cod') != "200":
            return f"Erreur : {data.get('message', 'Données météo non disponibles')}."
        forecast_list = []
        for forecast in data['list']:
            if "12:00:00" in forecast['dt_txt']:
                date = forecast['dt_txt'].split(" ")[0]
                forecast_info = {
                    'date': date,
                    'temperature': forecast['main']['temp'],
                    'description': forecast['weather'][0]['description']
                }
                forecast_list.append(forecast_info)
        return forecast_list[:5]
    except requests.exceptions.RequestException:
        return "Erreur : Impossible de récupérer les données météo."

def creer_icone_temporaire(texte):
    icone_path = "/tmp/meteo_temp.png"
    image_size = 128
    image = Image.new("RGBA", (image_size, image_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
    except IOError:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), texte, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (image_size - text_width) // 2
    y = (image_size - text_height) // 2
    draw.text((x, y), texte, fill="white", font=font)
    image.save(icone_path)
    return icone_path

def lire_ville_defaut():
    try:
        with open("ville_defaut.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def mettre_a_jour(indicateur, menu, ville):
    data = get_forecast(ville)
    if isinstance(data, str):
        icone_path = creer_icone_temporaire("Err")
        indicateur.set_icon(icone_path)
        for item in menu.get_children():
            menu.remove(item)
        item_erreur = Gtk.MenuItem(label=data)
        menu.append(item_erreur)
        item_erreur.show()
    else:
        temperature = int(data[0]['temperature'])
        texte = f"{temperature}°"
        icone_path = creer_icone_temporaire(texte)
        indicateur.set_icon(icone_path)
        for item in menu.get_children():
            menu.remove(item)
        for forecast in data:
            date = forecast["date"]
            temperature = forecast["temperature"]
            description = forecast["description"]
            label = f"{date}: {temperature}°C, {description}"
            item = Gtk.MenuItem(label=label)
            menu.append(item)
            item.show()
    item_quitter = Gtk.MenuItem(label="Quitter")
    item_quitter.connect("activate", Gtk.main_quit)
    menu.append(item_quitter)
    item_quitter.show()
    return True

def main():
    ville = lire_ville_defaut()
    indicator = AppIndicator3.Indicator.new(
        "meteo_indicator",
        "application-default-icon",
        AppIndicator3.IndicatorCategory.APPLICATION_STATUS
    )
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    menu = Gtk.Menu()
    item_quitter = Gtk.MenuItem(label="Quitter")
    item_quitter.connect("activate", Gtk.main_quit)
    menu.append(item_quitter)
    menu.show_all()
    indicator.set_menu(menu)
    mettre_a_jour(indicator, menu, ville)
    GLib.timeout_add_seconds(60, mettre_a_jour, indicator, menu, ville)
    Gtk.main()

if __name__ == "__main__":
    main()
