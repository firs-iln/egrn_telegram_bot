FROM python:3.11

RUN apt-get update
RUN apt-get install -y libglib2.0-0
RUN apt-get install -y libnss3
RUN apt-get install -y libgconf-2-4
RUN apt-get install -y libfontconfig1

ENV PYTHONUNBUFFERED=1

WORKDIR /bot

RUN pip install --upgrade pip

COPY requirements.txt /bot/

RUN pip install -r requirements.txt

COPY . /bot

RUN cd "bot" && \
    mkdir "files" && \
    mkdir "files/images" && \
    mkdir "files/received" && \
    mkdir "files/zips" && \
    mkdir "files/xlsx"
