# Wildlife Monitoring App

[![My Skills](https://skillicons.dev/icons?i=python,redis,docker,fastapi,pytorch)](https://skillicons.dev)

There is a web-service that offers you to uplpoad phtotos from camera traps and automatically detect wild animals with the following statistical information. The system is trained by ten sepecies describing Volgo-Kamsky Reserve: a lynx, bear, boar, fow, kelp gull, hare, badger, row deer, moose. 

![demo](https://downloader.disk.yandex.ru/preview/d9c028af8019f8afeb0744634cdd95abc957b14f04311aa0b72f013687d3c685/6a0e7288/u04fKWDQK3lh9RdvvMVxl0EJ-ti_A3RwX9feoKcYccEenYE6o1Ze2atIrYCjCdGq3Hx7NksPpLOTrCjgyJZPRQ%3D%3D?uid=0&filename=%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202026-05-11%20%D0%B2%2001.26.20.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v3&is_direct_zip_experiment=1&size=2048x2048)

# Content
* [Functuality](https://github.com/Mambulya/Wildlife-Monitoring-App/edit/main/README.md#1-functuality)
* Deploying and running
* Access
* Project Architecture

# 1 Functuality
UI and functuality demonstartion can be seen [here on YouTube](https://youtu.be/frzCHOC5gm4)

# 2 Deploying and running
To test the app, please, run the Docker Container Composition, described in `Dockerfile` and `docker-compose.yml`:
```console $
docker-compose up
```
# 3 Access
After that the service will be hosted on [localhost:8501](http://localhost:8501/)

# 4 Project Architecture
The progect consists of the following files:
```
|– app
|–––backend
|    |–__init__.py
|    |–classes_loader.py
|    |–image_processor.py
|    |–main.py
|    |–model_loader.py
|–––frontend
|    |–.streamlit
|	   |–config.toml
|    |–logo
|        |–app_icon.png
|        |–empty_folder.png
|        |–paws.png
|    |–pages
|        |–graphs.py
|        |–home.py
|    |–cache_loader.py
|	   |–main.py
|–––models
|    |–best8n.pt
|    |–classes.txt
|–––Dockerfile
|–––docker-compose.yml
|–––requirements.txt
```
