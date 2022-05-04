FROM python:3.8

RUN apt-get update

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD python manage.py makemigrations && python manage.py migrate && python manage.py loaddata data_rate