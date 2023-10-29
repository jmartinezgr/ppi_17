import os
import numpy as np
from skimage import io, color, transform
from sklearn import svm
from django.conf import settings

class VerificadorCarnetUNAL:
    def __init__(self, modelo_entrenado):
        self.modelo = modelo_entrenado

    def cargar_imagen(self, ruta_imagen):
        img = io.imread(ruta_imagen, as_gray=True)
        # Redimensionar la imagen si es necesario
        img = transform.resize(img, (100, 100)) 
        return img

    def verificar_carnet(self, ruta_imagen):
        imagen = self.cargar_imagen(ruta_imagen)
        imagen_vectorizada = imagen.reshape(1, -1)
        resultado = self.modelo.predict(imagen_vectorizada)
        return resultado[0] == 1  # 1 significa que es un carnet de la UNAL

# Escribe una función para entrenar el modelo y guárdalo en un archivo
def entrenar_modelo():
    # Paso 1: Cargar las imágenes y etiquetarlas
    images = []
    labels = []

    # Ruta a la carpeta de imágenes de carnets en el directorio 'media' de Django
    carpeta_carnets = os.path.join(settings.MEDIA_ROOT, 'carnet')

    for filename in os.listdir(carpeta_carnets):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            # Construir la ruta completa de la imagen
            ruta_imagen = os.path.join(carpeta_carnets, filename)

            # Cargar la imagen y etiquetarla
            img = io.imread(ruta_imagen, as_gray=True)
            img = transform.resize(img, (100, 100))
            images.append(img)
            labels.append(1)  # Etiqueta 1 para carnets

    # Ruta a la carpeta de imágenes que no son carnets en el directorio 'static' de Django
    carpeta_no_carnets = os.path.join(settings.STATIC_ROOT, 'imagenes_no_carnet')

    for filename in os.listdir(carpeta_no_carnets):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            # Construir la ruta completa de la imagen
            ruta_imagen = os.path.join(carpeta_no_carnets, filename)

            # Cargar la imagen y etiquetarla
            img = io.imread(ruta_imagen, as_gray=True)
            img = transform.resize(img, (100, 100))
            images.append(img)
            labels.append(0)  # Etiqueta 0 para no carnets

    # ... (carga de imágenes que no son carnets, similar a la versión original)

    # Paso 2: Preparar los datos para el entrenamiento
    X = np.array(images).reshape(len(images), -1)
    y = np.array(labels)

    # Paso 4: Entrenar un modelo de máquinas de soporte vectorial (SVM)
    clf = svm.SVC(kernel='linear')
    clf.fit(X, y)

    # Guardar el modelo en un archivo
    from joblib import dump
    ruta_modelo = os.path.join(settings.BASE_DIR, 'modelo_entrenado.joblib')
    dump(clf, ruta_modelo)

# Entrenar el modelo si no existe
if not os.path.exists(os.path.join(settings.BASE_DIR, 'modelo_entrenado.joblib')):
    entrenar_modelo()
