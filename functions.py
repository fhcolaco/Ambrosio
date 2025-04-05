import os
import pandas as pd
from geopy.geocoders import Photon
from city import City
import haversine as hs


def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


def parseTextFile(file, cached_locations):
    cities = []
    countryname = ""

    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        for line in lines:
            if line == lines[0]:
                countryname = line.strip()
                continue

            cityName, *connections = line.split(',')
            if (not any(cityName == city.getName() for city in cities)):
                cityLocation = getGeolocation(
                    cityName, cached_locations, countryname)
                city = City(cityName, cityLocation)
                cities.append(city)
            else:
                for index, c in enumerate(cities):
                    if c.getName() == cityName:
                        city = cities[index]

            for connection in connections:
                if '(' in connection:
                    connection_city = connection.split('(')[0].strip()
                    connection_distance = connection.split(
                        '(')[1].split(')')[0].strip()
                    connection_city_location = getGeolocation(
                        connection_city, cached_locations, countryname)
                else:
                    connection_city = connection.strip()
                    connection_city_location = getGeolocation(
                        connection_city, cached_locations, countryname)
                    connection_distance = round(hs.haversine(
                        city.getLocation(), connection_city_location))

                city.addConnection(
                    {"name": connection_city, "distance": connection_distance})
                if not any(connection_city == city.getName() for city in cities):
                    connectionCity = City(
                        connection_city, connection_city_location)
                    connectionCity.addConnection(
                        {"name": cityName, "distance": connection_distance})
                    cities.append(connectionCity)
                else:
                    for index, c in enumerate(cities):
                        if c.getName() == connection_city:
                            cities[index].addConnection(
                                {"name": cityName, "distance": connection_distance})

    with open("adittional_files/distancetofaro.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            cityname, distance = line.split(',')
            for index, c in enumerate(cities):
                if c.getName() == cityname:
                    cities[index].setStraightDistanceToFaro(distance.strip())
    return countryname, cities


def parseExcelFile(file, cached_locations):
    cities = []
    countryname = ""
    data = pd.read_excel(file, header=None)

    for index, row in data.iterrows():
        if index == 0:
            countryname = row[0]
            continue

        cityName = row[0]
        connections = row[1:]

        if not any(cityName == city.getName() for city in cities):
            cityLocation = getGeolocation(
                cityName, cached_locations, countryname)
            city = City(cityName, cityLocation)
            cities.append(city)
        else:
            for index, c in enumerate(cities):
                if c.getName() == cityName:
                    city = cities[index]

        for i, connection in enumerate(connections):
            if pd.notnull(connection):
                if '(' in connection:
                    connection_city = connection.split('(')[0].strip()
                    connection_distance = connection.split(
                        '(')[1].split(')')[0].strip()
                    connection_city_location = getGeolocation(
                        connection_city, cached_locations, countryname)
                else:
                    connection_city = connection.strip()
                    connection_city_location = getGeolocation(
                        connection_city, cached_locations, countryname)
                    connection_distance = round(hs.haversine(
                        city.getLocation(), connection_city_location))

                city.addConnection(
                    {"name": connection_city, "distance": connection_distance})
                if not any(connection_city == city.getName() for city in cities):
                    connectionCity = City(
                        connection_city, connection_city_location)
                    connectionCity.addConnection(
                        {"name": cityName, "distance": connection_distance})
                    cities.append(connectionCity)
                else:
                    for index, c in enumerate(cities):
                        if c.getName() == connection_city:
                            cities[index].addConnection(
                                {"name": cityName, "distance": connection_distance})
    return countryname, cities


def loadCachedLocations():
    cached_locations = []
    open("adittional_files/cached_locations.txt", "a").close()
    with open("adittional_files/cached_locations.txt", "r", encoding="utf-8") as file:
        for line in file:
            location, latitude, longitude = line.split(',')
            cached_locations.append({"location": location, "latitude": float(
                latitude), "longitude": float(longitude)})
    return cached_locations


def getGeolocation(location, cached_locations, country=""):
    if location in [loc["location"] for loc in cached_locations]:
        # print(f"Using cached location for {location}.")
        cached_location = next(
            (loc for loc in cached_locations if loc["location"] == location), None)
        return [cached_location["latitude"], cached_location["longitude"]]
    # print(f"Geolocating {location}...")
    geolocator = Photon(user_agent="ia202324")
    geolocation = geolocator.geocode(
        location + ", " + country if country != "" else location)
    cached_locations.append(
        {"location": location, "latitude": geolocation.latitude, "longitude": geolocation.longitude})
    with open("adittional_files/cached_locations.txt", "a", encoding="utf-8") as file:
        file.write(
            f"{location},{geolocation.latitude},{geolocation.longitude}\n")
    return [geolocation.latitude, geolocation.longitude]


def h(start_city, end_city):
    if (end_city.getName() == "Faro"):
        return int(start_city.getStraightDistanceToFaro())
    return int(hs.haversine(start_city.getLocation(), end_city.getLocation()))
