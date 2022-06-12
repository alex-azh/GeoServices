import OpenRouteService.API as API
import Graphics.Html
import Tests.staticData as static
points=[static.perm2,static.park,static.stolica]
route=API.GetDistanceLineBoundTime(points)
print("Расстояние (км)", route["distance"])
print("BoundingBox",route["bound"])
print("Время (мин)", route["time"])
Graphics.Html.GeoService(mainPoints=points,
                         polyPoints=route["line"],
                         namePage="openrouteservice.html",
                         service="openrouteservice")

