from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.responses import StreamingResponse, HTMLResponse
from typing import List
import zipfile
import uvicorn
import io

from app.backend.model_loader import load_model
from app.backend.image_processor import image_process_with_YOLO
from app.backend.classes_loader import load_classes

# экземпляр приложения
app = FastAPI(title="Animals Detection API for Monitoring Wildlife",
              description="Upload photos by camera traps and get YOLO detection results",
              contact={"name": "Anna Yashnova",
                       "url": "https://github.com/Mambulya",
                       "email": "anyashnova@kpfu.ru"})


# load model once ar startup
MODEL = load_model()
CLASSES_STR = load_classes()
MODEL_VERSION = "YOLOv8n"

@app.get("/", summary="Home page", description="Welcome to the Animals Detection API for Monitoring Wildlife!")
def home():
    # """
    # Render the main page of the API
    # """
    # return "Hello!\nWelcome to the Animals Detection API for Monitoring Wildlife!"
        content = """
    <body>
    <form action="/detect/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    </body>
        """
        return HTMLResponse(content=content)



@app.post("/detect/")
async def detect(files: List[UploadFile] = File(...)):
    """
    Take photos from user and detect animals using YOLO model.

    :param files: Upload images

    :returns: detected images with its label data via txt file.

    :raises HTTPException: 

        if no image is uploaded, the HTTP Error 415 raises.

        if any error during YOLO detecion is occured, the HTTP Error 400 raises.
    """
    if len(files) == 0 or len(files) > 100:
        raise HTTPException(status_code=400, detail="Please upload between 1 and 100 images.")
    
    # zip buffer creation
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        zip_file.writestr(f"classes.txt", CLASSES_STR)
        for file in files:
                file_bytes = await file.read()
                filename = file.filename
                if filename.endswith((".png", ".jpg", ".jpeg")):
                    try:
                        pred_bytes, label_file = image_process_with_YOLO(img=file_bytes, model=MODEL)
                        base_file_name = filename.rsplit(".", 1)[0]
                        # не создаются файлы на диске, а собирается архив прямо 
                        # в оперативной памяти, чтобы сразу отправить его клиенту!
        
                        zip_file.writestr(f"images/{base_file_name}.jpg", pred_bytes)
                        zip_file.writestr(f"labels/{base_file_name}.txt", label_file)

                    except Exception as e:
                        raise HTTPException(status_code=400, detail=f"Exception during YOLO detection has raised: {str(e)}")
                else:
                    raise HTTPException(status_code=415, detail="Unsupported file type. Please upload an image.")
        
    zip_buffer.seek(0) # cursor at start position for correct reading the archive

    return StreamingResponse(content=zip_buffer, 
                                     media_type="application/zip",
                                     headers={"Content-Disposition": "attachment; filename=detection.zip"})


#if __name__ == "__main__":
    ##### обычный запуск #####
    # fastapi dev main.py
    # иначе 
    # uvicorn main:app --reload
    #
    # иначе
   #uvicorn.run("main:app", reload=True)
   # или
   # app.run(debug=True, host="0.0.0.0")
