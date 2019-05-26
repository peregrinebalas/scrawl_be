FROM python:3

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV DJANGO_SETTINGS_MODULE=my_django_project.settings \
    PYTHONPATH=/usr/src/app SECRET_KEY=1 DATABASE_URL=

# download GeoIP database
RUN wget -qO- http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz \
    | gunzip > /srv/GeoLite2-City.mmdb
env GEOIP_PATH=/srv/GeoLite2-City.mmdb

# debian packages: GeoDjango dependencies
RUN apt-get update && \
    apt-get install -y binutils libproj-dev gdal-bin && \
    rm -rf /var/lib/apt/lists/*

# python packages
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# django apps & manage
COPY my_django_project /usr/src/app/my_django_project
COPY my_django_app /usr/src/app/my_django_app
COPY my_other_django_app /usr/src/app/my_other_django_app
COPY manage.py /usr/src/app/manage.py

RUN ./manage.py collectstatic --no-input

# Heroku doesn't like EXPOSE
#EXPOSE 8000

CMD gunicorn my_django_project.wsgi:application --bind=0:$PORT --access-logfile=- --error-logfile=-
EOF
