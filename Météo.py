import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import csv
import requests
import datetime


def GetCoord(name):
    longitude = 0
    latitude = 0
        
    filename = "CityGPS.csv"

    # Vérifier si la ville existe déjà dans le fichier CSV
    ville_exists = False

    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Sauter l'en-tête
        for row in reader:
            if row[0].lower() == name.lower():  # Comparer les noms de villes en ignorant la casse
                ville_exists = True
                latitude = row[1]
                longitude = row[2]
                break

    if not ville_exists:
        # Ouvrir le fichier en mode append (ajout)
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            # Ajouter l'en-tête si le fichier n'existe pas
            if file.tell() == 0:  # file.tell() renvoie 0 si le fichier est vide
                writer.writerow(["Ville", "Latitude", "Longitude"])
                
            # Écrire les données de la ville
            api_url = 'https://api.api-ninjas.com/v1/city?name={}'.format(name)
            response = requests.get(api_url, headers={'X-Api-Key': 'KjQis/qNBqiaUaKxJizU2A==s6cqc3493DhIjwM0'})
            if response.status_code == requests.codes.ok:
                data = response.json()
                if data:  # Vérifiez si des données ont été renvoyées
                    longitude = data[0]["longitude"]
                    latitude = data[0]["latitude"]
                    ville_data = [name, latitude, longitude]
                    writer.writerow(ville_data)
                else:
                    print(f"Aucune donnée trouvée pour la ville {name}.")
                    return None  # Sortir si aucune donnée n'est trouvée
            else:
                print("Erreur lors de l'appel à l'API:", response.status_code, response.text)
                return None  # Sortir en cas d'erreur API
                
    return GetTemp(longitude, latitude)

def GetTemp(longitude, latitude):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
        "daily": ["sunrise", "sunset"],
        "timezone": "auto",
        "forecast_days": 7
    }
    responses = openmeteo.weather_api(url, params=params)

    # Vérifiez si la réponse contient des données
    if not responses:
        print("Aucune réponse de l'API Open-Meteo.")
        return None

    # Process first location
    response = responses[0]

    # Process hourly data
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )
    }
    hourly_data["temperature_2m"] = hourly_temperature_2m

    hourly_dataframe = pd.DataFrame(data=hourly_data)

    date = datetime.datetime.now().date()
    hour = datetime.datetime.now().hour

    # Par exemple, si vous voulez la température à une heure spécifique
    specific_time = pd.Timestamp(f'{date} {hour}:00:00', tz='UTC')

    # Accéder à la ligne correspondant à cette date/heure
    temp_values = hourly_dataframe[hourly_dataframe['date'] == specific_time]['temperature_2m']

    daily = response.Daily()
    daily_sunrise = daily.Variables(0).ValuesAsNumpy()
    daily_sunset = daily.Variables(1).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
    )}
    daily_data["sunrise"] = daily_sunrise
    daily_data["sunset"] = daily_sunset

    daily_dataframe = pd.DataFrame(data = daily_data)

    print(daily_dataframe)

    if not temp_values.empty:  # Vérifiez si temp_values n'est pas vide
        temperature_at_specific_time = temp_values.values[0]
        return temperature_at_specific_time
    else:
        print(f"Aucune température trouvée pour {specific_time}.")
        return None  # Sortir si aucune température n'est trouvée



