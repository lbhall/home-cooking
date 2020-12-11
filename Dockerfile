FROM python:3

ADD code/ /app
WORKDIR /app

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python app.py --host 0.0.0.0