FROM python:3

RUN mkdir -p /code
WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=scrawl_be.settings
ENV PYTHONPATH=/code


# download GeoIP database
RUN wget -qO- http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz \
    | gunzip > /srv/GeoLite2-City.mmdb
env GEOIP_PATH=/srv/GeoLite2-City.mmdb

# debian packages: GeoDjango dependencies
RUN curl --silent https://bootstrap.pypa.io/get-pip.py | python3.7
RUN apt-get update && \
    apt-get install -y binutils libproj-dev gdal-bin postgresql-client-10 && \
    rm -rf /var/lib/apt/lists/*

# django apps & manage
COPY scrawl_be /code/scrawl_be
COPY scrawls /code/scrawls
COPY manage.py /code/manage.py

# python packages
RUN pip install pipenv
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --system
RUN pipenv install django

CMD gunicorn scrawl_be.wsgi:application
