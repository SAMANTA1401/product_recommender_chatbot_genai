FROM python:3.10-slim-buster

RUN  echo "enter docker file"

WORKDIR /app

COPY . /app

RUN echo "copy all fiel to WORKDIR"

RUN apt update -y && apt install awscli -y

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 unzip -y && pip install -r requirements.txt

RUN echo "installed requirements.txt"

CMD ["python3", "app.py"]