# scrawl_be

As [Turing School of Software & Design](https://turing.io/)'s final group project in the backend program, we built an application in collaboration with the frontend program. This repository is the code base for the Django-based backend for the our application Scrawl. The backend handles requests to our postgres db with a postgis extension for geolocation-based queries.

## Python & Django Versions

Python 3.7.3
Django 2.2.1

## Setup & Installation

### Database

for the database you'll need to extend your postgres with postgis
postgis comes with it's own dependancies to install them with homebrew run
```
$ brew install postgresql
$ brew install postgis
$ brew install gdal
$ brew install libgeoip
```
additional install instructions can be found [here](https://docs.djangoproject.com/en/2.2/ref/contrib/gis/install/#homebrew).
After all dependancies are installed create a Postgres db
```
$ createdb scrawl_database
$ psql scrawl_database
> CREATE EXTENSION postgis;
```

### Application

If you don't already have pipenv installed run
`$ pip install pipenv`
after that run
`$ pipenv install`
to install all dependancies.

after that run
`pipenv run python manage.py migrate`
to run all migrations to the database.

## API Endpoints



