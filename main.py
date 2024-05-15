from fastapi import FastAPI, UploadFile, File, HTTPException
import uvicorn
from PIL import Image
import io
import boto3
from models.super_resolution import enhance_image_resolution

app = FastAPI()

s3_client = boto3.client('s3')
bucket_name = 'tu-bucket-s3'

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

        # Subir la imagen mejorada a S3
        s3_client.upload_fileobj(buffer, bucket_name, f"enhanced/{file.filename}")

        return {"filename": file.filename, "status": "Image enhanced and uploaded to S3"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
