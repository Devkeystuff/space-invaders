# Get the official image
FROM python:3.10.1-buster

# Set working directory
WORKDIR /app

# Copy requirements to working directory
COPY requirements.txt .

# For postgres configuration
RUN apt-get -y install postgresql-12 postgresql-client
RUN apt-get -y install python3-dev libpq-dev
RUN apt-get update

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]