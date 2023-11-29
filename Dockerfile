FROM python:3.11

RUN apt-get install -y libglib2.0-0=2.50.3-2 \
    libnss3=2:3.26.2-1.1+deb9u1 \
    libgconf-2-4=3.2.6-4+b1 \
    libfontconfig1=2.11.0-6.7+b1

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
