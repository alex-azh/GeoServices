import MathModule as MathModule

html="""<html>
<title>Routing</title>

<head>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.8.0/dist/leaflet.css" integrity="sha512-hoalWLoI8r4UszCkZ5kL8vayOGVae1oxXe/2A4AO6J9+580uKHDO3JdHb7NzwwzK5xr/Fs0W40kiNHxM9vyTtQ==" crossorigin="" />
  <script src="https://unpkg.com/leaflet@1.8.0/dist/leaflet.js" integrity="sha512-BB3hKbKWOc9Ez/TAwyWxNXeoV9c1v6FIeYiBieIWkpLjauysF18NzgR1MBNBXf8/KABdlkX68nAhlwcDFLGPCQ==" crossorigin=""></script>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.3.1/dist/leaflet.css" integrity="sha512-Rksm5RenBEKSKFjgI3a41vrjkw4EVPlJ3+OiI65vTjIdo9brlAacEuKOiQ5OFh7cOI1bkDwLqdLw3Zg0cRJAAQ==" crossorigin="" />
  <script src="https://unpkg.com/leaflet@1.3.1/dist/leaflet.js" integrity="sha512-/Nsx9X4HebavoBvEBuyp3I7od5tA0UzAxs+j83KgC8PU0kgB4XiK4Lfe4y4cgBtaRJQEIFCW+oC506aPT2L1zw==" crossorigin=""></script>
</head>

<body>
  <div id="map" style="width: 100%; height: 100%;"></div>
  <script>
    var map = L.map('map');
    var latLon = L.latLng($center$);
    var bounds = latLon.toBounds($meters$); // 500 = metres
    map.panTo(latLon).fitBounds(bounds);
    var tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    var polylinePoints = [
    $points$
    ];
    var polyline = L.polyline(polylinePoints).addTo(map);
    L.layerGroup([
    $markers$
    ]).addTo(map);
  </script>
</body>

</html>"""

def HtmlGenerator(mainPoints,points):
    """
    Заполнить шаблон маркерами и полилинией.
    :param points: Точки в (lon,lat).
    :return:
    """
    markerks=""
    polyline=""
    # диагональная точка на boundingbox
    b=MathModule.BoundCalculate(points) # l,b,r,t
    p1X,p1Y=b[0],b[1]
    p2X,p2Y=b[2],b[3]
    center=((p1X+p2X)/2,(p1Y+p2Y)/2)
    meters=MathModule.FixedFloat(MathModule.DistanceCalculate(longA=p1X,latA=p1Y,longB=p2X,latB=p2Y),0)
    for point in points:
       polyline+=f",[{point[1]}, {point[0]}]"
    for point in mainPoints:
        markerks += f",L.marker([{point[1]}, {point[0]}])"
    return html.replace("$markers$",markerks[1:]).replace("$points$",polyline[1:]).replace("$center$",f"{center[1]},{center[0]}").replace("$meters$",f"{meters}")


