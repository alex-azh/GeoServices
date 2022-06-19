from KEY import mainKey
import requests
from urllib.parse import quote

url="https://eu1.locationiq.com/v1/search.php?key={0}&q={1}&format=json&accept-language=ru"
def Parser(l):
    if type(l)==list:
        l=l[0]
        if type(l)==dict:
            if l.get("lat") and l.get("lon"):
                return [float(l["lon"]),float(l["lat"])]
    pass

def Geocoder(s: str):
    """
    Получить координаты объекта по его адресу.
    :param s: адрес объекта
    :return: (долгота, широта)
    """
    s=quote(s)
    r=requests.get(url=url.format(mainKey,s))
    if r.status_code==200:
        return Parser(r.json())
