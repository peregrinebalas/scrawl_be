# scrawl_be

Hosted by Heroku at: https://scrawlr.herokuapp.com

Scrawl's frontend repo can be found at: https://github.com/TomWilhoit/scrawl_fe

As [Turing School of Software & Design](https://turing.io/)'s final group project in the backend program, we built an application in collaboration with the frontend program. This repository is the code base for the Django-based backend for the our application Scrawl. The backend handles requests to our postgres db with a postgis extension for geolocation-based queries.

## Python & Django Versions

Python 3.7.3
Django 2.2.1

## Postgis Database Schema

![postgis schema](https://files.slack.com/files-pri/T029P2S9M-FJT1E0J9Y/screen_shot_2019-05-30_at_8.19.08_am.png)

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

### POST to Walls
`https://scrawlr.herokuapp.com/api/v1/walls`

Request
```
{
  "name": "Your Wall's Name",
  "lat": 39.7507827,
  "lng": -104.9966852,
  "comment": "Optional Comment"
}
```

201 Response
```
{
    "pk": 8,
    "name": "Your Wall's Name",
    "lat": 39.7507827,
    "lng": -104.9966852,
    "comments": [
        "Optional Comment"
    ]
}
```

409 Response
```
{
    "error": "Fields missing, could not save wall."
}
```

### GET for Wall Show
`https://scrawlr.herokuapp.com/api/v1/walls/:id`

200 Response
```
{
    "pk": 8,
    "name": "Your Wall's Name",
    "lat": 39.7507827,
    "lng": -104.9966852,
    "comments": [
        "Optional Comment",
        "Second Comment",
        "Third Comment",
        "See the pattern?" 
    ]
}
```

404 Response
```
{
    "error": "Could Not Find Wall"
}
```

### GET for Nearest Walls Index
`https://scrawlr.herokuapp.com/api/v1/walls/nearest?lat=39.7507827&lng=-104.9966852`

200 Response
```
[
  {
      "pk": 8,
      "name": "Your Wall's Name",
      "lat": 39.7507827,
      "lng": -104.9966852
  },
  {
      "pk": 7,
      "name": "Farther Away Wall",
      "lat": 39.8507827,
      "lng": -105.9966852
  },
    {
      "pk": 10,
      "name": "Even Farther Away Wall",
      "lat": 40.8507827,
      "lng": -106.2466852
  }
]
```

404 Response
```
{
    "error": "Cannot Locate Nearest Walls"
}
```

### POST to Wall's Comments
`https://scrawlr.herokuapp.com/api/v1/walls/:id/comments`

Request
```
{
    "comment": "New comment"
}
```

201 Response
```
{
    "message": "Comment Saved!"
}
```

409 Response
```
{
    "error": "Conflict!"
}
```
