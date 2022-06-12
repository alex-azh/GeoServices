import Graphics.Html
from DoubleGis.API import DistanceLineBoundTimeBy2GIS
import Tests.staticData as static

points=[static.perm2,static.park,static.stolica]
route= DistanceLineBoundTimeBy2GIS(points=points)

print("Расстояние (км)", route["distance"])
print("BoundingBox",route["bound"])
print("Время (мин)", route["time"])
Graphics.Html.GeoService(mainPoints=points,
                         polyPoints=route['line'],
                         namePage="2gis.html",
                         service="doublegis")
