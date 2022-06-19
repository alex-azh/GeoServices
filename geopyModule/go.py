from geopy.geocoders import Nominatim

def Geocoder(s: str):
    """
    Получить координаты объекта по его адресу.
    :param s: адрес объекта
    :return: (долгота, широта)
    """
    geolocator = Nominatim(user_agent="Mozilla Firefox 36 (Win 8.1 x64): Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0")
    location = geolocator.geocode(s)
    if location:
        return [location.longitude,location.latitude]