import os
import geopandas as gpd
from shapely.geometry import Point

def calcular_punto_medio(lat1, lon1, lat2, lon2):
    """
    Calcula el punto medio geográfico entre dos coordenadas.

    Dada la latitud y longitud de dos puntos, este método utiliza la biblioteca GeoPandas
    para crear un GeoDataFrame con esos puntos y calcular el punto medio geográfico.

    Args:
        lat1 (float): Latitud del primer punto.
        lon1 (float): Longitud del primer punto.
        lat2 (float): Latitud del segundo punto.
        lon2 (float): Longitud del segundo punto.

    Returns:
        list: Una lista que contiene las coordenadas [latitud, longitud] del punto medio.
    """
    # Crear un GeoDataFrame con dos puntos
    gdf = gpd.GeoDataFrame(geometry=[Point(lon1, lat1), Point(lon2, lat2)], crs="EPSG:4326")

    # Calcular el punto medio
    punto_medio = gdf.unary_union.centroid

    # Obtener las coordenadas del punto medio
    lat_medio, lon_medio = punto_medio.y, punto_medio.x

    return [lat_medio, lon_medio]









