import os
import geopandas as gpd
from shapely.geometry import Point

def calcular_punto_medio(lat1, lon1, lat2, lon2):
    # Crear un GeoDataFrame con dos puntos
    gdf = gpd.GeoDataFrame(geometry=[Point(lon1, lat1), Point(lon2, lat2)], crs="EPSG:4326")

    # Calcular el punto medio
    punto_medio = gdf.unary_union.centroid

    # Obtener las coordenadas del punto medio
    lat_medio, lon_medio = punto_medio.y, punto_medio.x

    return [lat_medio, lon_medio]








