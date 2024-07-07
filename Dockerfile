FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install aiogram
RUN pip install aiomysql
RUN pip install beautifulsoup4
RUN pip install lxml
RUN pip install cryptography
RUN pip install pymysql
RUN chmod 755 .

CMD ["python", "init_db.py"]

