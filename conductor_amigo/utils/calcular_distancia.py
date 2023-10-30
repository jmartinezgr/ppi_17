import os
import geopandas as gpd
from shapely.geometry import Point

def calcularDistacia (coord_inicio, coord_destino):

    # Definir dos puntos que deseas medir (como coordenadas latitud y longitud)
    coordenada1 = Point(coord_inicio[0],coord_inicio[1])
    coordenada2 = Point(coord_destino[0], coord_destino[1])

    # Calcular la distancia entre los dos puntos
    distancia = coordenada1.distance(coordenada2)

    result = {
        "coordenada_inicial": coordenada1,
        "coordenada_final": coordenada2,
        "distancia": distancia
    }
    
    return result








