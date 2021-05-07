# syntax=docker/dockerfile:1

FROM python:3.8

RUN apt update && \
  apt install wget && \
  apt install curl && \
  apt install unzip
RUN wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
RUN unzip ./ngrok-stable-linux-amd64.zip
RUN pip3 install pipenv

WORKDIR /app
COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install

COPY . .

ENTRYPOINT ["pipenv", "run", "python", "configure_and_run.py"]
