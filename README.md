# scrawl_be

Hosted by Heroku at: https://scrawlr.herokuapp.com

Scrawl's frontend repo can be found at: https://github.com/TomWilhoit/scrawl_fe

As [Turing School of Software & Design](https://turing.io/)'s final group project in the backend program, we built an application in collaboration with the frontend program. This repository is the code base for the Django-based backend for the our application Scrawl. The backend handles requests to our postgres db with a postgis extension for geolocation-based queries.

## Python & Django Versions

Python 3.7.3
Django 2.2.1

## Postgis Database Schema

![postgis schema](https://lh3.googleusercontent.com/W1dMS84KvCdPuYFeGfpLA6SaATo616IU79AbbNTsa3nsXft_MriXEkEg5FCG4cVDrGWv3ib3E_Aezm0tuLyh0QlB-rRh-o1fl8A1oAn8h17iYcFfGfBUmfwZneiwl6CEVxQJZczxXvAxL5EAnW2L-GhvB2iMXrsTsRB-XtzFR1q9jd5sWQN0z0EtKztOHz5ZxNk4ZqT78bNkfNhTxKDmCB6_PWYJqo-s1oSm9WovZZy-wuKM2pxPaQ3waUL45eNq5rLPuPg4gXaxLpHnucQXgGL-OuEn5guIge2czEeAOsCSObRcwKJjnM02Ivc7AjCx7GEARRpZjudbpeZNkL0Uaqs0mO7BC1bKIo0XMj9JQQYDfKGTxC95HUqmT-0sBwdj-KhSPmXbtEQBiOOFWAWUabojE0SZ5MQvjSZ11EsxLacODvv_Ed9ZQieDXTux0OqWz6z5dxMIMeitrM56z_lewnI_8jP6ibPAXPDgFpC4-2iaDE6WIQ8jjSVssFsoJMV-IaekZI6_2WgcgXT5dWsmR9br_ZB_TFVm5eHlaDdq3nDEgeF0cbvMDeqSYW5KbdHCToqPxVbyMHbMe-0AmXlIrE18D3pTTzSUAHUDpsQXWVs6rltKIWf8EsN-rbYm5uYufx8mcVPC44xJARIYxYDMI1bZ5VPCRM8=w1078-h470-no)

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

### Contributors
[Peregrine Balas](https://github.com/PeregrineReed)
[Scott Thomas](https://github.com/smthom05)
[Peregrine Balas](https://github.com/TomWilhoit)
