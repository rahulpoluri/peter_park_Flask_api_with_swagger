FROM python:3
WORKDIR /code
RUN apt update -y
RUN apt upgrade -y
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code/
