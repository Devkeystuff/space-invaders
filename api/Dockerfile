FROM python:3.10-buster

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python
RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY . .

CMD python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload