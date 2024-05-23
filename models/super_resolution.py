from PIL import Image
import numpy as np
import cv2
import os
import logging

logger = logging.getLogger(__name__)

def enhance_image_resolution(image: Image.Image) -> Image.Image:
    """
    Mejora la resolución de la imagen utilizando el modelo EDSR de OpenCV.
    """
    try:
        # Convertir la imagen a RGB si no lo está
        if image.mode != "RGB":
            image = image.convert("RGB")
        logger.info("Image converted to RGB")

        # Convertir la imagen a un array de numpy
        image_np = np.array(image)
        logger.info("Image converted to numpy array")

        # Crear el objeto de superresolución
        super_res_model = cv2.dnn_superres.DnnSuperResImpl_create()

        # Verificar que el archivo del modelo existe
        model_path = os.path.join(os.path.dirname(__file__), '../EDSR_x4.pb')  # Ajusta la ruta según sea necesario
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"El archivo del modelo no se encontró: {model_path}")
        logger.info(f"Model file found at {model_path}")

        # Leer el modelo preentrenado
        super_res_model.readModel(model_path)
        logger.info("Model loaded successfully")

        # Establecer el modelo para la escala x4
        super_res_model.setModel("edsr", 4)
        logger.info("Model set for scale x4")

        # Aplicar el modelo para mejorar la resolución
        logger.info("Applying super resolution model...")
        enhanced_image_np = super_res_model.upsample(image_np)
        logger.info("Image resolution enhanced")

        # Convertir el array de numpy de vuelta a una imagen PIL
        enhanced_image = Image.fromarray(enhanced_image_np)
        logger.info("Enhanced image converted back to PIL format")

        return enhanced_image

    except Exception as e:
        logger.error(f"Error enhancing image resolution: {e}", exc_info=True)
        raise
