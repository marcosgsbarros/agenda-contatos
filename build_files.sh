#! bin/bash

echo "construindo o projeto"
python -m pip install -r requirements.txt


echo "fazendo migrations"
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "coletar static"
python manage.py collectstatic --noinput --clear

