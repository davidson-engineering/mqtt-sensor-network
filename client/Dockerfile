FROM python:3-slim

RUN apt-get update && apt-get install -y
RUN apt-get install git -y
RUN python -m pip install --upgrade pip

COPY ./ /app
WORKDIR /app
RUN pip install .