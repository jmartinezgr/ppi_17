import os
import numpy as np
from skimage import io, color, transform
from sklearn import svm
from django.conf import settings

class VerificadorCarnetUNAL:
    """
    Clase que utiliza un modelo entrenado para verificar si una imagen corresponde a un carnet de la UNAL.

    Attributes:
        modelo_entrenado: El modelo previamente entrenado, compatible con la predicción de imágenes.

    Methods:
        cargar_imagen(ruta_imagen): Carga una imagen dada su ruta, la redimensiona y la devuelve.
        verificar_carnet(ruta_imagen): Verifica si la imagen dada por la ruta es un carnet de la UNAL.
    """

    def __init__(self, modelo_entrenado):
        self.modelo = modelo_entrenado

    def cargar_imagen(self, ruta_imagen):
        """
        Carga una imagen dada su ruta, la redimensiona y la devuelve.

        Args:
            ruta_imagen (str): La ruta de la imagen a cargar.

        Returns:
            ndarray: La imagen cargada y redimensionada.
        """
        img = io.imread(ruta_imagen, as_gray=True)
        img = transform.resize(img, (100, 100)) 
        return img

    def verificar_carnet(self, ruta_imagen):
        """
        Verifica si la imagen dada por la ruta es un carnet de la UNAL.

        Args:
            ruta_imagen (str): La ruta de la imagen a verificar.

        Returns:
            bool: True si la imagen es un carnet de la UNAL, False en caso contrario.
        """
        imagen = self.cargar_imagen(ruta_imagen)
        imagen_vectorizada = imagen.reshape(1, -1)
        resultado = self.modelo.predict(imagen_vectorizada)
        return resultado[0] == 1  # 1 significa que es un carnet de la UNAL

def entrenar_modelo():
    """
    Entrena un modelo de máquinas de soporte vectorial (SVM) para la detección de carnets de la UNAL.

    Este método carga imágenes de carnets y no carnets, las etiqueta, y entrena un modelo SVM.
    Finalmente, guarda el modelo entrenado en un archivo.

    Returns:
        None
    """
    # Paso 1: Cargar las imágenes y etiquetarlas
    images = []
    labels = []

    # ... (código de carga de imágenes, similar a la versión original)

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

