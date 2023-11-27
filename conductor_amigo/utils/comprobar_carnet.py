import cv2
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim

def cargar_imagen(ruta):
    imagen = cv2.imread(ruta)
    imagen = cv2.resize(imagen, (300, 300))
    return cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)  # Convertir a escala de grises

def es_carnet_nuevo(imagen_nueva, imagenes_exist):
    for imagen_exist in imagenes_exist:
        # Normalizar imágenes
        nueva_normalizada = cv2.normalize(imagen_nueva, None, 0, 255, cv2.NORM_MINMAX)
        existente_normalizada = cv2.normalize(imagen_exist, None, 0, 255, cv2.NORM_MINMAX)

        # Comparar histogramas
        correlacion_histograma = cv2.compareHist(cv2.calcHist([nueva_normalizada], [0], None, [256], [0, 256]),
                                                 cv2.calcHist([existente_normalizada], [0], None, [256], [0, 256]), cv2.HISTCMP_CORREL)

        # Comparar SSIM
        ssim_index, _ = compare_ssim(nueva_normalizada, existente_normalizada, full=True)

        # Ajusta estos valores según sea necesario
        if correlacion_histograma > 0.8 and ssim_index > 0.8:
            return True

    return True
