# zestimate.py

from geopy.geocoders import Nominatim

address = "426 S CLARA AVENUE DELAND FL 32720"

app = "PAMS"

def geo_coordinates(address):

    geolocator = Nominatim(user_agent=app)
    location = geolocator.geocode(address)

    return location.latitude, location.longitude

def geo_address(address):

    geolocator = Nominatim(user_agent=app)
    location = geolocator.geocode(address)

    return location.address


if __name__ == "__main__":

    full_address = geo_address(address)
    _lat, _long = geo_coordinates(address)

    print(full_address)
    print((_lat, _long,))