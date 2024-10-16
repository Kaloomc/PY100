import requests
import csv
# Définir la latitude et la longitude



def currentWeather(latitude,longitude):

    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,is_day,precipitation,rain,snowfall,cloud_cover"
    response = requests.get(url)
    data = response.json()
    return data

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
    return latitude,longitude


