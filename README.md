# Wildlife Monitoring App

[![My Skills](https://skillicons.dev/icons?i=python,redis,docker,fastapi,pytorch)](https://skillicons.dev)

Веб-сервис, который предлагает вам загружать фотографии с камер-ловушек и автоматически обнаруживать диких животных со следующей статистической информацией на основе поддержки модели YOLO8 nano. Система обучена по десяти подвидам, описывающим Волго-Камский заповедник: рысь, медведь, кабан, белка, чайка, заяц, барсук, косуля, лось, лисица.


# Содержание
* [Функциональность](#1-functuality)
* [Развертывание и запуск](#2-deploying-and-running)
* [Доступ](#3-access)
* [Архитектура проекта](#4-project-architecture)

# 1 Функциональность
Увидеть демонстрацию пользовательского интерфейса и функционала можно [здесь на YouTube](https://youtu.be/frzCHOC5gm4)

# 2 Deploying and running
Чтобы протестировать приложение, пожалуйста, запустите Docker движок и композицию контейнеров, описанную в `Dockerfile` и `docker-compose.yml`:
```console $
docker-compose up
```
# 3 Доступ
После этого приложение будет работать в локальной сети по адресу [localhost:8501](http://localhost:8501/)

# 4 Архитектура проекта
Проект состоит из следующих файлов:
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
