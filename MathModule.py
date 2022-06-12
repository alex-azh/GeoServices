import math
import re

def DistanceCalculate(latA, longA, latB, longB):
    """
    Расстояние между координатами.
    Координаты указываются противоположно тем, которые заходят в яндекс.
    :return:
    """
    EARTH_RADIUS = 6372795
    lat1 = latA * math.pi / 180;
    lat2 = latB * math.pi / 180;
    long1 = longA * math.pi / 180;
    long2 = longB * math.pi / 180;
    a = math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(long2 - long1));
    return EARTH_RADIUS * a

def FixedFloat(number, digit=6):
    if type(number)==float or type(number)==int:
        if digit==0:
            return int(number)
        s=str(number)
        return float(s[:s.find('.')+digit+1])
    else:
        return 0

def ToFloatParserLINESTRING(s: str):
    """
    Распарсивает LINESTRING у 2GIS по точкам. Однако точки в самом методе приходят в (широта, долгота).
    Этот парсер возвращает значения по (долгота, широта)
    :param s:
    :return: (долгота, широта) (float,float)
    """
    s = s[s.find('(') + 1:s.find(')')]
    numbers = [float(s) for s in re.findall(r'-?\d+\.?\d*', s)]
    # создать пары чисел - координаты
    j = 1
    # print(numbers)
    while (j <= len(numbers)):
        yield (numbers[j - 1], numbers[j])
        j += 2

def BoundCalculate(points):
    """
    Посчитать boundingbox по точкам.
    :param points: Точки в 2Д системе координат.(x,y)
    :return: (minX,minY,maxX,maxY)
    """
    l=9999
    r=-9999
    t=-9999
    b=9999
    for point in points:
        x=point[0]
        y=point[1]
        l=min(l,x)
        r=max(r,x)
        t=max(t,y)
        b=min(b,y)
    return l,b,r,t

