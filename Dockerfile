FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN pip install --upgrade pip

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY /code  /code

RUN mkdir "files" && \
    mkdir "files/images" && \
    mkdir "files/received" && \
    mkdir "files/zips" && \
    mkdir "files/xlsx"
