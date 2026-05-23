# Wildlife Monitoring App

[![My Skills](https://skillicons.dev/icons?i=python,redis,docker,fastapi,pytorch)](https://skillicons.dev)

Веб-сервис, который предлагает вам загружать фотографии с камер-ловушек и автоматически обнаруживать диких животных со следующей статистической информацией на основе поддержки модели YOLO8 nano. Система обучена по десяти подвидам, описывающим Волго-Камский заповедник: рысь, медведь, кабан, белка, чайка, заяц, барсук, косуля, лось.

![demo](https://3.downloader.disk.yandex.ru/preview/c593bc523f3dd07856d0bbe97a711d63ead263be7325d59e464fc86bcbcdfbbb/inf/zbqgBam49X6LeCPrwkWEGh3nBZGXrTaeicf8R_5UvaSruybeQ3lN8aq71CyCk-OncPezarO_iSH_jSGuSJtD_Q%3D%3D?uid=743031542&filename=%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202026-05-23%20%D0%B2%2018.39.51.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=743031542&tknv=v3&is_direct_zip_experiment=1&size=2850x1624)

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
