from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import uvicorn
import io

from model_loader import load_model
from image_processor import image_process_with_YOLO

# экземпляр приложения
app = FastAPI(title="Animals Detection API for Monitoring Wildlife",
              description="Upload photos by camera traps and get YOLO detection results",
              contact={"name": "Anna Yashnova",
                       "url": "https://github.com/Mambulya",
                       "email": "anyashnova@kpfu.ru"})


# load model once ar startup
MODEL = load_model()
MODEL_VERSION = "YOLOv8n"

@app.get("/", summary="Home page", description="Welcome to the Animals Detection API for Monitoring Wildlife!")
def home():
    """
    Render the main page of the API
    """
    return "Hello!\nWelcome to the Animals Detection API for Monitoring Wildlife!"


@app.post("/detect/")
async def detect(file: UploadFile):
    """
    Take a photo from user and detect animals using YOLO model.
    :param file: Upload an image

    :returns: a detected image with its label data via txt file.
    :raises HTTPException: if not image is uploaded, the HTTP Error 415 raises.
                           if any error during YOLO detecion is occured, the HTTP Error 400 raises.
    """

    file_bytes = await file.read()
    filename = file.filename

    if filename.endswith((".png", ".jpg", ".jpeg")):
        try:
            pred_bytes = image_process_with_YOLO(img=file_bytes, model=MODEL)
            return StreamingResponse(content=io.BytesIO(pred_bytes), media_type="image/jpeg")
        except Exception as e:
            raise HTTPException(status_code=400, detail="Exception during YOLO detection has raised")
    else:
        raise HTTPException(status_code=415, detail="Unsupported file type. Please upload an image.")



if __name__ == "__main__":
    ##### обычный запуск #####
    # fastapi dev api.py
    # иначе 
    # uvicorn api:app --reload
    #
    # иначе
   uvicorn.run("main:app", reload=True)
