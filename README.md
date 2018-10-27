# matchday-server

## Requirements

* virtualenv

* python3


## Usage

cd into project root directory

### Preparation to using virtualenv
Make sure that you have python3 installed. 

Create separated environment
```
$ virtualenv -p python3 venv
```
Activate separated envirionment
```
$ source venv/bin/activate
```
Deactivate separated environment(while virtualenv is activated)
```
$ deactivate
```
### Install required packages
while virtualenv is active
```
$ pip3 install django
$ pip3 install django-rest-framework
$ pip3 install coreapi
```
### Run Aplication
```
create postgresql database
create database user
$ export DB_NAME=<your database name>
$ export DB_USER=<your database user name>
$ export DB_PASS=<your database user password>
$ export DJANGO_SETTINGS_MODULE=matchday-server.settings.production
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py runserver
```

### Run Tests
```
$ export DJANGO_SETTINGS_MODULE=matchday-server.settings.dev
$ python3 manage.py test --parallel
```
