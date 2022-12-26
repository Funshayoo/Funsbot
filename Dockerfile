FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y ffmpeg

CMD [ "python3", "main.py" ]
