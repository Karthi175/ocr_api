# syntax=docker/dockerfile:1

FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /ocr_docker


COPY requirements.txt requirements.txt

COPY . .


RUN apt-get update \
&& apt-get -y install tesseract-ocr \
&& apt-get install tesseract-ocr-eng \
&& apt-get install -y python3 python3-distutils python3-pip \
&& cd /usr/local/bin \
&& ln -s /usr/bin/python3 python \
&& pip3 --no-cache-dir install --upgrade pip \
&& rm -rf /var/lib/apt/lists/*


RUN apt-get update \
&& apt-get install -y python3-opencv

RUN apt-get update \
&& apt-get install -y poppler-utils

RUN apt update \
&& apt-get install ffmpeg libsm6 libxext6 -y

RUN pip3 install pytesseract


RUN pip3 install -r requirements.txt

ENV LC_ALL=C.UTF-8

ENV LANG=C.UTF-8

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]