FROM python:2.7-alpine
MAINTAINER Inumidun Amao <ashamao90@gmail.com>

ENV INSTALL_PATH /meet-n-eat
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUP pip install -r requirements.txt

COPY . .

CMD gunicorn -b 0.0.0.0:8000 --access-logfile 'meet-n-eat.manage.runserver()'
