FROM python:3.10

WORKDIR /hms_backend
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . ./
