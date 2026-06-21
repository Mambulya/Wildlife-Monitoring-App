# Wildlife Monitoring App

[![My Skills](https://skillicons.dev/icons?i=python,redis,docker,fastapi,pytorch)](https://skillicons.dev)

There is a web-service that offers you to upload photos from camera traps and automatically detect wild animals with the following statistical information. The system is trained by ten species describing Volgo-Kamsky Reserve: a lynx, bear, boar, fox, kelp gull, hare, badger, row deer, moose, squirrel.

# Content
* [Functuality](#1-functuality)
* [Deploying and running](#2-deploying-and-running)
* [Access](#3-access)
* [Project Architecture](#4-project-architecture)

# 1 Functuality
UI and functuality demonstration can be seen [here on YouTube](https://youtu.be/frzCHOC5gm4)

# 2 Deploying and running
To test the app, please, run the Docker Container Composition, described in `Dockerfile` and `docker-compose.yml`:
```console $
docker-compose up
```
# 3 Access
After that the service will be hosted on [localhost:8501](http://localhost:8501/)

# 4 Project Architecture
The project consists of the following files:
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
