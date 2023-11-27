import cv2
import numpy as np
from scipy.signal import correlate2d

def cargar_imagen(ruta):
    imagen = cv2.imread(ruta)
    imagen = cv2.resize(imagen, (300, 300))
    return imagen

def es_carnet_nuevo(imagen_nueva, imagenes_exist):
    for imagen_exist in imagenes_exist:
        correlacion = comparar_imagenes(imagen_nueva, imagen_exist)
        if correlacion > 0.8:
            return True
    return False

def comparar_imagenes(imagen1, imagen2):
    # Usar la correlación cruzada 2D de SciPy
    resultado_correlacion = correlate2d(imagen1, imagen2, boundary='symm', mode='same')
    mejor_correlacion = np.max(resultado_correlacion)
    return mejor_correlacion
