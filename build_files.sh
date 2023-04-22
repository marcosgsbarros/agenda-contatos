#! bin/bash

echo "contruindo o projeto"
python3.11 -m pip install -r requirements.txt


echo "fazendo migrations"
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "coletar static"
python manage.py collectstatic --noinput --clear

