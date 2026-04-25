FROM python:3.13

# системные зависимости для OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# отключить буферизацию вывода для отображения логов
ENV PYTHONUNBUFFERED=1 

WORKDIR /code

ENV PYTHONPATH=/code

COPY ./app /code/app
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
