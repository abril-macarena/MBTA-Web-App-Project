import os 
import json
import urllib.parse
import urllib.request
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API keys from environment variables
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")

# Useful base URLs (you need to add the appropriate parameters for each API request)
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"


# A little bit of scaffolding if you want to use it
def get_json(url: str) -> dict:
    """
    Given a properly formatted URL for a JSON web API request, return a Python JSON object containing the response to that request.

    Both get_lat_lng() and get_nearest_station() might need to use this function.
    """
    with urllib.request.urlopen(url) as response:
        response_text = response.read().decode("utf-8")
        data = json.loads(response_text)
    return data


def get_lat_lng(place_name: str) -> tuple[str, str]:
    """
    Given a place name or address, return a (latitude, longitude) tuple with the coordinates of the given place.

    See https://docs.mapbox.com/api/search/geocoding/ for Mapbox Geocoding API URL formatting requirements.
    """
    encoded_place_name = urllib.parse.quote(place_name)
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{encoded_place_name}.json?access_token={MAPBOX_TOKEN}&types=poi"
    data = get_json(url)
    coordinates = data["features"][0]["geometry"]["coordinates"]
    longitude, latitude = coordinates[0], coordinates[1]
    return str(latitude), str(longitude)


def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool]:
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible) tuple for the nearest MBTA station to the given coordinates.

    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL formatting requirements for the 'GET /stops' API.
    """
    url = f"https://api-v3.mbta.com/stops?filter[latitude]={latitude}&filter[longitude]={longitude}&sort=distance&api_key={MBTA_API_KEY}"
    data = get_json(url)
    station_info = data["data"][0]["attributes"]
    station_name = station_info["name"]
    wheelchair_accessible = station_info["wheelchair_boarding"] == 1
    return station_name, wheelchair_accessible


def find_stop_near(place_name: str) -> tuple[str, bool]:
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.

    This function might use all the functions above.
    """
    latitude, longitude = get_lat_lng(place_name)
    return get_nearest_station(latitude, longitude)


def main():
    """
    You should test all the above functions here
    """
    place_name = "Newburry Street"
    station_name, is_wheelchair_accessible = find_stop_near(place_name)
    print(f"Nearest MBTA stop to {place_name}: {station_name}")
    print(f"Wheelchair accessible: {'Yes' if is_wheelchair_accessible else 'No'}")



if __name__ == "__main__":
    main()
