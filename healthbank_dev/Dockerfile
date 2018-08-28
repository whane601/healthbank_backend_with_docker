FROM python:3.6.2
LABEL maintainer twtrubiks
ENV PYTHONUNBUFFERED 1
RUN mkdir /healthbank_api
WORKDIR /healthbank_api
COPY . /healthbank_api/
RUN pip install -r requirements.txt
RUN pip install psycopg2
RUN apt-get update
RUN apt-get install -y \
    vim