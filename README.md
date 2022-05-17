shipments-api
=============

### Introduction:
REST API for shipments.

### Requirements:
* Python 3.9
* Django 4.0
* DRF 3.13

### Installation:
* Clone repo:
```bash
git clone https://github.com/jrafa/shipments-api.git
```
* Install requirements:
```bash
pipenv install
```
* Copy credentials:
```bash
cp env/local.env .env
```
* Run docker-compose postgres db:
```bash
docker-compose -f docker-compose.db.yml up -d
```
* Run migration:
```bash
python manage.py migrate
```
* Run locally by PyCharm IDE or in terminal:
```bash
python manage.py runserver
```
* Run tests:
```bash
coverage run --source='.' manage.py test api
coverage report
```