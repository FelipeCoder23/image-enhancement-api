from fastapi import FastAPI, UploadFile, File, HTTPException
import uvicorn
from PIL import Image
import io
from models.super_resolution import enhance_image_resolution  # Asegúrate de que esta ruta sea correcta
import logging
import os

# Configurar el registro de errores
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/enhance-image/")
async def enhance_image(file: UploadFile = File(...)):
    try:
        # Leer la imagen subida
        image = Image.open(file.file)

        # Mejorar la resolución de la imagen usando el modelo de IA
        enhanced_image = enhance_image_resolution(image)

        # Guardar la imagen mejorada en un buffer
        buffer = io.BytesIO()
        enhanced_image.save(buffer, format="PNG")
        buffer.seek(0)

        # Guardar localmente para pruebas
        output_filename = f"enhanced_{file.filename}"
        output_filepath = os.path.abspath(output_filename)
        with open(output_filepath, "wb") as f:
            f.write(buffer.getbuffer())

        # Devolver la ruta completa del archivo mejorado
        return {"filename": output_filepath, "status": "Image enhanced and saved locally"}

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to enhance image: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
