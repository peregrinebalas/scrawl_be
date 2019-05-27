FROM python:3

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV DJANGO_SETTINGS_MODULE=scrawl_be.settings \
    PYTHONPATH=/usr/src/app SECRET_KEY=1 DATABASE_URL=


# download GeoIP database
RUN wget -qO- http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz \
    | gunzip > /srv/GeoLite2-City.mmdb
env GEOIP_PATH=/srv/GeoLite2-City.mmdb

# debian packages: GeoDjango dependencies

RUN curl --silent https://bootstrap.pypa.io/get-pip.py | python3.7
RUN apt-get update && \
    apt-get install -y binutils libproj-dev gdal-bin && \
    rm -rf /var/lib/apt/lists/*

# python packages
RUN pip install pipenv
COPY Pipfile Pipfile.lock /usr/src/app/
RUN pipenv install --system

# django apps & manage
COPY scrawl_be /usr/src/app/scrawl_be
COPY scrawls /usr/src/app/scrawls
COPY manage.py /usr/src/app/manage.py

CMD gunicorn scrawl_be.wsgi:application --bind=0:$PORT
