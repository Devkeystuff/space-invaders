FROM python:3.10-buster

WORKDIR /srv/app

RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python
RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY . .
