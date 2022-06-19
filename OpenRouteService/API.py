import openrouteservice
from openrouteservice import convert
from OpenRouteService.API_KEYS import token

def GetDistanceLineBoundTime(points)->dict:
    """
    Получить длину, линию, прямоугольную область и время маршрута.
    :param points: Точки, по которым строится маршрут.
    :return: {"distance": d, "line": l, "bound": b, "time": t}
    """
    try:
        client = openrouteservice.Client(key=token)  # Specify your personal API key
        routes = client.directions(points)
        geometry = routes['routes'][0]['geometry']
        decoded = convert.decode_polyline(geometry)
        l = list(map(lambda x: [x[1], x[0]], decoded["coordinates"]))
        d, b, t = routes["routes"][0]["summary"]["distance"], routes["routes"][0]["bbox"], \
                  routes["routes"][0]["summary"]["duration"]
        return {"distance": d/1000, "line": l, "bound": b, "time": t/60}
    except OSError as ex:
        print(ex.strerror)
        return False

def ParserDict(s):
    if type(s)==dict:
        if s.get("features"):
            if len(s["features"])>0:
                if type(s["features"][0])==dict:
                    if s["features"][0].get("geometry"):
                        if s["features"][0]["geometry"].get("coordinates"):
                            return s["features"][0]["geometry"]["coordinates"]

def GeoCoder(address: str):
    """
    Получить координаты точки по её адресу.
    :param address: вводимый пользователем адрес
    :return: (долгота,широта)
    """
    try:
        client = openrouteservice.Client(key=token)
        r=openrouteservice.client.pelias_search(client,address)
        if r:
            return ParserDict(r)
        return False
    except:
        return False
        print("Ошибка GeoCoder()")


