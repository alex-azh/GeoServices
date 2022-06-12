import Graphics.templates.openrouteservice_html as routeHTML
import Graphics.templates.DoubleGisService_html as doubleGisHTML

def GeoService(mainPoints, polyPoints, namePage, service: str):
    "Метод для создания html файла на основе созданного geo-сервиса"
    try:
        if service.lower()=="openrouteservice":
            page=routeHTML.HtmlGenerator(mainPoints=mainPoints,points=polyPoints)
        elif service.lower()=="doublegis":
            page=doubleGisHTML.HtmlGenerator(mainPoints=mainPoints,points=polyPoints)
        with open(namePage, "w") as file:
            file.write(page)
        return True
    except OSError as ex:
        return False