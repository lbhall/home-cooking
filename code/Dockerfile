FROM python:3

ADD . /app
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python app.py --host 0.0.0.0