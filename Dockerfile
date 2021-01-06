# создать образ на основе базового слоя python (там будет ОС и интерпретатор Python)
FROM python:3.8.5

LABEL author='praktikum@yandex.ru' version=1 broken_keyboards=5

# создать директорию /code
RUN mkdir /code

# скопировать всё содержимое директории, в которой лежит докерфайл, в директорию /code
COPY . /code

# установить в качестве текущей директорию /code
WORKDIR /code

# выполнить команду (как в терминале, с тем же синтаксисом) для установки пакетов из requirements.txt
RUN pip install -r requirements.txt

# выполняем миграции
# RUN python manage.py migrate

# заполняем базу начальными данными
# RUN python manage.py loaddata fixtures

# запуск приложения через gunicorn 
CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
