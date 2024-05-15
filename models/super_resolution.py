from PIL import Image
import numpy as np
import cv2

def enhance_image_resolution(image: Image.Image) -> Image.Image:
    """
    Mejora la resolución de la imagen utilizando el modelo EDSR de OpenCV.
    """
    # Convertir la imagen a un array de numpy
    image_np = np.array(image)

    # Crear el objeto de superresolución
    super_res_model = cv2.dnn_superres.DnnSuperResImpl_create()

    # Leer el modelo preentrenado
    super_res_model.readModel('EDSR_x4.pb')  # Ruta al modelo preentrenado de EDSR

    # Establecer el modelo para la escala x4
    super_res_model.setModel("edsr", 4)

    # Aplicar el modelo para mejorar la resolución
    enhanced_image_np = super_res_model.upsample(image_np)

    # Convertir el array de numpy de vuelta a una imagen PIL
    enhanced_image = Image.fromarray(enhanced_image_np)

    return enhanced_image
