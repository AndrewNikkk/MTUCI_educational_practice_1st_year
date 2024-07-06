FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install aiogram
RUN pip install aiomysql
RUN pip install beautifulsoup4
RUN pip install lxml

CMD ["python", "bot.py"]

#FROM mysql:latest
#
#ENV MYSQL_DATABASE marvel
#ENV MYSQL_ROOT_PASSWORD = 12MAR
#
#COPY ./init.sql/ /docker-entrypoint-initdb.d/
