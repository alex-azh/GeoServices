import datetime
import DoubleGis.API as DAPI
import OpenRouteService.API as OpenRouteAPI


class RouteService(object):
    def __init__(self, points: list):
        self.points = points
        self.distance = None
        self.line = None
        self.bound = None
        self.time = None

    def DistanceLineBoundTime_By2GIS(self) -> dict:
        """
        Обновить расстояние(км), линию, прямоугольную область и время(мин) по указанному маршруту в 2GIS
        :return: dict('distance','line',bound,time)
        """
        r = DAPI.DistanceLineBoundTimeBy2GIS(self.points)
        self.distance = r["distance"]
        self.time = r["time"]
        self.bound = r["bound"]
        self.line = r["line"]

    def DistanceLineBoundTime_ByOpenRoute(self) -> dict:
        """
        Обновить расстояние(км), линию, прямоугольную область и время(мин) по указанному маршруту в 2GIS
        :return: dict('distance','line',bound,time)
        """
        r = OpenRouteAPI.GetDistanceLineBoundTime(self.points)
        self.distance = r["distance"]
        self.time = r["time"]
        self.bound = r["bound"]
        self.line = r["line"]

    def CreateHtml(self, filename: str, service: str):
        from Graphics.Html import GeoService
        GeoService(mainPoints=self.points, polyPoints=self.line, namePage=filename, service=service)
