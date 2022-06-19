import requests as req
import json

import MathModule

h = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, utf-8'",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/json;charset=UTF-8",
    "dnt": "1",
    "origin": "https://2gis.ru",
    "referer": "https://2gis.ru/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
}
data = {
    "locale": "ru",
    "point_a_name": "Source",
    "point_b_name": "Target",
    "purpose": "autoSearch", "type": "online5",
}


def PointToJsonData(arr):
    """
    Преобразовать массив точек в json.
    X - долгота, Y - широта у точек в массиве arr.
    :param arr: массив точек (x,y). X - долгота, Y - широта
    :return:
    """
    points = []
    for point in arr:
        # х - долгота(lon), y - широта(lat)
        points.append(
            {
                "type": "pref",
                "x": point[0],
                "y": point[1],
            }
        )
    # у первой и споледней изменить type на pedo
    points[0]["type"] = "pedo"
    points[len(points) - 1]["type"] = "pedo"
    return points


def GISWay(data):
    """
    Запрос в 2GIS по поиску маршруту на машине.
    :param data: тело запроса типа dict.
    :return: Точки в самом результате в виде (широта, долгота).
    """
    r = req.post('https://catalog.api.2gis.ru/carrouting/6.0.0/global?key=rurbbn3446', headers=h, data=json.dumps(data),
                 stream=True)
    if r.status_code == 200:
        return {"status": True, "r": json.loads(r.text)}
    else:
        return {"status": False, "server": f"code={r.status_code};{r.text}"}


def DistanceLineBoundTimeBy2GIS(points):
    """
    Получить BoundingBox по 2GIS
    :param startPoint: (lon,lat)
    :param endPoint: (lon,lat)
    :return:(minX,minY,maxX,maxY), Distance
    """
    dataPoints = PointToJsonData(points)
    mydata = data.copy()
    mydata.update({"points": dataPoints})
    response = GISWay(mydata)
    if response["status"] == True:
        try:
            response = response["r"]
            # выбираем первый результат путей
            way = dict(response["result"][0])
            nabors = way["maneuvers"][0]["outcoming_path"]["geometry"]
            Distance = way['total_distance']/1000
            totalTime=way['total_duration']/60
            l = 9999
            r = -9999
            t = -9999
            b = 9999
            polyPoints=[]
            for part in nabors:  # part: участок пути
                for point in MathModule.ToFloatParserLINESTRING(part["selection"]):
                    l, r, t, b = min(l, point[0]), max(r, point[0]), max(t, point[1]), min(b, point[1])
                    polyPoints.append(point)
            return {"distance": Distance, "line": polyPoints, "bound": (l,b,r,t),"time":totalTime}
        except OSError as ex:
            return False
    else:
        # задекларировать ошибку в бд
        return False
