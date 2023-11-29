FROM joyzoursky/python-chromedriver:3.9

# set display port to avoid crash
ENV DISPLAY=:99

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
    mkdir "files/xlsx" && \
    mkdir "parser/parse_website/captchas"
