# Wildlife Monitoring App


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
