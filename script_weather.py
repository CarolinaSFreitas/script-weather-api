import os
from dotenv import load_dotenv
import requests
import time

load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        response.raise_for_status()
        ip = response.json()["ip"]
        return ip
    except requests.RequestException as e:
        print(f"Erro ao obter IP público: {e}")
        return None

def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        response.raise_for_status()
        data = response.json()
        return data["city"], data["region"], data["country"]
    except requests.RequestException as e:
        print(f"Erro ao obter localização: {e}")
        return None, None, None

def get_weather(city, state, country):
    try:
        url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&lang=pt"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        condition = data["current"]["condition"]["text"].lower()
        temperature = data["current"]["temp_c"]
        
        weather_emojis = {
            "sol": "☀️ ",
            "ensolarado": "☀️ ",
            "parcialmente nublado": "🌤️ ",
            "nublado": "☁️ ",
            "chuva": "🌧️ ",
            "neblina": "🌫️ ",
            "trovoada": "⛈️ ",
            "neve": "❄️ "
        }
        
        emoji_icon = "🌈"
        for key in weather_emojis:
            if key in condition:
                emoji_icon = weather_emojis[key]
                break

        print(f"{emoji_icon} Tempo em {city.title()} - {state} - {country}: {condition.capitalize()}, {temperature}°C")
        
    except requests.RequestException as e:
        print(f"Erro ao obter clima: {e}")
    except KeyError:
        print("Erro: dados inesperados recebidos da WeatherAPI.")

# lua
def get_astronomy(city):
    try:
        url = f"https://api.weatherapi.com/v1/astronomy.json?key={API_KEY}&q={city}&lang=pt"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        moon_phase = data["astronomy"]["astro"]["moon_phase"]
        moon_emojis = {
            "New Moon": "🌑 Lua nova",  
            "Waxing Crescent": "🌒 Lua crescente", 
            "First Quarter": "🌓 Quarto crescente",  
            "Waxing Gibbous": "🌔 Gibosa crescente",  
            "Full Moon": "🌕 Lua cheia", 
            "Waning Gibbous": "🌖 Gibosa minguante", 
            "Last Quarter": "🌗 Quarto minguante",  
            "Waning Crescent": "🌘 Lua minguante"  
        }

        moon_info = moon_emojis.get(moon_phase, "Fase da lua desconhecida")

        print(f"Fase da lua hoje: {moon_info}")
        
    except requests.RequestException as e:
        print(f"Erro ao obter dados astronômicos: {e}")
    except KeyError:
        print("Erro: dados inesperados recebidos da WeatherAPI.")

def main():
    ip = get_public_ip()
    if not ip:
        return

    city, state, country = get_location(ip)
    if not city or not state or not country:
        return

    while True:
        get_weather(city, state, country)
        get_astronomy(city)  
        time.sleep(30)

if __name__ == "__main__":
    main()