from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.responses import StreamingResponse, HTMLResponse
from pydantic import BaseModel
import json

from typing import List

import zipfile
import redis
import hashlib
import io

from app.backend.model_loader import load_model
from app.backend.image_processor import image_process_with_YOLO
from app.backend.classes_loader import load_classes, load_classes_list


######### App and Database linking #########

app = FastAPI(title="Animals Detection API for Monitoring Wildlife",
              description="Upload photos by camera traps and get YOLO detection results",
              contact={"name": "Anna Yashnova",
                       "url": "https://github.com/Mambulya",
                       "email": "anyashnova@kpfu.ru"})

client = redis.Redis(host="localhost",
                    # host="redis",      # Docker service name
                     port=6379, 
                     db=0
                     )

if client.ping() == False:
     raise ConnectionError("Radis Cache Database is not connected. Please, run Redis before by 'redis-server'")

###########################


######## Constants ########

MODEL = load_model()
CLASSES_STR = load_classes()
CLASSES_LIST = load_classes_list()
MODEL_VERSION = "YOLOv8n"

CACHE_SECONDS_LIMIT = 600
# CACHE_SECONDS_LIMIT = 3600

###########################

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



@app.post("/detect/", summary="Uploading, detecting and caching images", description="Here you can work with input")
async def detect(files: List[UploadFile] = File(...)) -> StreamingResponse:
    """
    Take photos from user and detect animals using YOLO model + caches predictions in Redis DataBase 
            img_{filename}: {'animals': 'int;int;...',
                            ...}

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
                        base_file_name = filename.rsplit(".", 1)[0]
                        pred_bytes, label_file = image_process_with_YOLO(img=file_bytes, model=MODEL)

                        # кэширование предсказаний модели
                        file_hash = hashlib.md5(base_file_name.encode()).hexdigest()
                        cached_key = f"img:{file_hash}"

                        if not client.exists(cached_key):
                             value_info = {'animals': dict()}

                             for pred in label_file.split("\n"):
                                  if pred:
                                       animal_name = CLASSES_LIST[int(pred.split()[0])]
                                       value_info["animals"][animal_name] = value_info["animals"].get(animal_name, 0) + 1

                             client.set(name=cached_key, 
                                        value=json.dumps(value_info),
                                        ex=CACHE_SECONDS_LIMIT)

                        # не создаются файлы на диске, а собирается архив прямо 
                        # в оперативной памяти, чтобы сразу отправить его клиенту!
        
                        zip_file.writestr(f"images/{base_file_name}.jpg", pred_bytes)
                        zip_file.writestr(f"labels/{base_file_name}.txt", label_file)

                    except Exception as e:
                        raise HTTPException(status_code=400, detail=f"Exception during YOLO detection or caching has raised: {str(e)}")
                else:
                    raise HTTPException(status_code=415, detail="Unsupported file type. Please upload an image.")
        
    zip_buffer.seek(0) # cursor at start position for correct reading the archive

    return StreamingResponse(content=zip_buffer, 
                                     media_type="application/zip",
                                     headers={"Content-Disposition": "attachment; filename=detection.zip"})


class StatsRequest(BaseModel):
    file_names: List[str]


@app.post("/stats/", summary="Getting cache", description="Getting predictions cache for statistics for session")
async def get_stats(request: StatsRequest):
    """
     Takes predictions for each image from keys.

     :param file_names: files name for which statistics is needed: image_1.jpg

     :returns: dictionary of images and their predictions
     
    """
    all_statistics = list()

    for file_name in request.file_names:
        base_file_name = file_name.rsplit(".", 1)[0]
        key = f"img:{hashlib.md5(base_file_name.encode()).hexdigest()}"

        value_json = client.get(key)

        if value_json:
            try:
                  data = json.loads(value_json)

            except json.JSONDecodeError:
                 continue
            
            all_statistics.append(data)

    return all_statistics
        





    

     


#if __name__ == "__main__":
    ##### обычный запуск #####
    # redis-server              
    # fastapi dev main.py
    # иначе 
    # uvicorn main:app --reload
    #
    # иначе
   #uvicorn.run("main:app", reload=True)
   # или
   # app.run(debug=True, host="0.0.0.0")
