FROM python:3.6-jessie

RUN echo "deb http://archive.debian.org/debian jessie main" > /etc/apt/sources.list
RUN apt-get update
RUN apt-get install software-properties-common less vim -y --force-yes

ENV INSTALL_PATH /mqtt_pwn
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
