FROM python:3.6-jessie

RUN apt-get update
RUN apt-get install software-properties-common less vim -y

ENV INSTALL_PATH /mqtt_pwn
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
