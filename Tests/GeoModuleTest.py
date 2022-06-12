from GeoClass import RouteService

perm2 = [56.18378, 58.00472]
park=[56.24653,58.00372]
stolica=[56.18762,57.97829]
v = RouteService([perm2,park,stolica])
v.DistanceLineBoundTime_By2GIS()
print("Расстояние в км:",v.distance)
print("BoundingBox",v.bound)
v.CreateHtml("GeoModuleTest.html","doublegis")