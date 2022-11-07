import requests as req
import json
import urllib.parse

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
            Distance = way['total_distance'] / 1000
            totalTime = way['total_duration'] / 60
            l = 9999
            r = -9999
            t = -9999
            b = 9999
            polyPoints = []
            for part in nabors:  # part: участок пути
                for point in MathModule.ToFloatParserLINESTRING(part["selection"]):
                    l, r, t, b = min(l, point[0]), max(r, point[0]), max(t, point[1]), min(b, point[1])
                    polyPoints.append(point)
            return {"distance": Distance, "line": polyPoints, "bound": (l, b, r, t), "time": totalTime}
        except OSError as ex:
            return False
    else:
        # задекларировать ошибку в бд
        return False


def GetPointByAddress(address: str):
    safe_string = urllib.parse.quote_plus(address)
    url = f'https://catalog.api.2gis.ru/3.0/suggests?key=rurbbn3446&q={safe_string}&viewpoint1=56.16714564705952,57.965217576345275&viewpoint2=56.187058352940475,57.96217842365471&fields=items.name_ex,items.rubrics,items.org,items.adm_div,items.routes,items.type,items.subtype,items.address,items.search_attributes.personal_priority,items.search_attributes.dgis_source_type,items.search_attributes.dgis_found_by_address,items.segment_id,items.region_id,items.locale,items.group,items.context,search_attributes,items.flags,items.has_exchange,items.ads.options&type=adm_div.region,adm_div.district_area,adm_div.city,adm_div.settlement,adm_div.district,adm_div.living_area,adm_div.division,adm_div.place,street,branch,building,road,attraction,crossroad,route,route_type,station,station.metro,user_queries,attribute,rubric,meta_rubric,org,market.category,market.attribute,market.suggestor_category,special,coordinates,kilometer_road_sign&search_device_type=desktop&search_user_hash=7221910362830496868&locale=ru_RU&stat[sid]=ff5d0b45-d6e0-4751-8a68-6d00388a9c5b&stat[user]=dd906a9d-8c4c-420e-b658-27889e3d5faa&shv=2022-11-02-17&r=3387366170'
    urlPoint='https://catalog.api.2gis.ru/3.0/items/byid?id={}&key=rurbbn3446&locale=ru_RU&fields=items.locale,items.flags,search_attributes,items.adm_div,items.city_alias,items.region_id,items.segment_id,items.reviews,items.point,request_type,context_rubrics,query_context,items.links,items.name_ex,items.org,items.group,items.dates,items.external_content,items.contact_groups,items.comment,items.ads.options,items.email_for_sending.allowed,items.stat,items.stop_factors,items.description,items.geometry.centroid,items.geometry.selection,items.geometry.style,items.timezone_offset,items.context,items.level_count,items.address,items.is_paid,items.access,items.access_comment,items.for_trucks,items.is_incentive,items.paving_type,items.capacity,items.schedule,items.floors,ad,items.rubrics,items.routes,items.platforms,items.directions,items.barrier,items.reply_rate,items.purpose,items.attribute_groups,items.route_logo,items.has_goods,items.has_apartments_info,items.has_pinned_goods,items.has_realty,items.has_exchange,items.has_payments,items.has_dynamic_congestion,items.is_promoted,items.congestion,items.delivery,items.order_with_cart,search_type,items.has_discount,items.metarubrics,broadcast,items.detailed_subtype,items.temporary_unavailable_atm_services,items.poi_category,items.structure_info.material,items.structure_info.floor_type,items.structure_info.gas_type,items.structure_info.year_of_construction,items.structure_info.elevators_count,items.structure_info.is_in_emergency_state,items.structure_info.project_type&viewpoint1=56.17397716080768,57.96654227640353&viewpoint2=56.18384521288348,57.958233537961604&stat[sid]=ff5d0b45-d6e0-4751-8a68-6d00388a9c5b&stat[user]=dd906a9d-8c4c-420e-b658-27889e3d5faa&shv=2022-11-02-17&r=3373357464'
    r = req.post(url=url, headers=h)
    r = json.loads(r.text)
    r: dict
    if r.get('result') == None:
        return False
    if r.get('result').get('items') == None:
        return False
    l = r['result']['items']
    if r.get('result').get('search_attributes')==None:
        return False
    points=r['result']['search_attributes']
    if points.get('drag_bound')==None:
        return False
    result=[]
    for i in range(0,len(l)-1):
        if l[i].get('full_name')==None:
            return False
        full_name=l[i].get('full_name')
        if l[i].get('address')==None:
            return False
        building_id=l[i]['address']['building_id']
        building_url=urlPoint.format(building_id)
        tmp_r=req.get(url=building_url,headers=h)
        building=json.loads(tmp_r.text)
        try:
            tmp_spisok=building['result']['items']
            for build in tmp_spisok:
                if build['address']['building_id']==building_id:
                    s=build['geometry']['centroid']
                    dva=s[s.find('(')+1:s.rfind(')')].split(' ')
                    long=float(dva[0])
                    lat=float(dva[1])
                    result.append([full_name,[long,lat]])
                    break
        except OSError as ex:
            print(ex.strerror)
            print(result)
            return False
    print(result)


