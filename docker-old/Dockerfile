from ubuntu:precise
MAINTAINER Emil Lamm Nielsen

# Install packages
RUN apt-get update
RUN apt-get build-dep -y build-essential
RUN apt-get install -y build-essential git libpq-dev
RUN apt-get install -y binutils libproj-dev gdal-bin
RUN apt-get install -y nginx supervisor
RUN apt-get install -y python python-dev python-setuptools

# install uwsgi
RUN easy_install pip
RUN pip install uwsgi

# install nginx
RUN apt-get install -y python-software-properties
#RUN apt-get update
RUN add-apt-repository -y ppa:nginx/stable

ADD requirements/common.txt /server/requirements/common.txt
ADD requirements/production.txt /server/requirements/production.txt
RUN pip install -r /server/requirements/production.txt

# deploy code
ADD . /server/

# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /server/nginx-app.conf /etc/nginx/sites-enabled/
RUN ln -s /server/supervisor-app.conf /etc/supervisor/conf.d/

ENV PYTHONPATH /server:$PYTHONPATH
ENV DJANGO_SETTINGS_MODULE impaqd_server.settings.production

#!/bin/bash
# This hook is sourced after this virtualenv is activated.

#ENV PYTHONPATH /d/mercedes-backend/
#ENV DJANGO_SETTINGS_MODULE impaqd_server.settings.development
ENV DJANGO_SETTINGS_MODULE impaqd_server.settings.production
#ENV DATABASE_URL postgis://SAMBUCA:@localhost/tempdb
#ENV DATABASE_URL postgis://imp2dat:FuBar401da@sandboxdb.traansmission.com/traansmissionsandboxdb
#ENV DATABASE_URL postgis://imp2dat:FuBar401da@demodb.traansmission.com/traansmissiondemodb
ENV NOTIFICATION_EMAIL emil@traansmission.com
ENV HOST http://localhost:8000
ENV CERTIFICATE sandbox-prod
ENV CELERY_BROKER_URL amqp://emil:emil1234@ec2-52-6-165-114.compute-1.amazonaws.com:5672//
#ENV CELERY_BROKER_URL amqp://traansrabbit:IpaApi101ra@messages-sandbox.services.traansmission.com:5672//
ENV SECRET_KEY 1234567
ENV POSTGIS_VERSION 2 1
ENV TEST_DATABASE_URL postgis://SAMBUCA:@localhost/traansmission-test
ENV PORTAL_URL http://localhost:9000/#/
ENV AWS_ACCESS_KEY_ID AKIAJ2BKKRRUGO6ZKQFQ
ENV AWS_SECRET_ACCESS_KEY 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
ENV S3_BUCKET_PREFIX local-emil
ENV DEBUG true
ENV TOS_CURRENT_VERSION 1


# Python

# RUN (mkdir /server/impaqd_server/static)
#RUN (cd /server/ && python manage.py collectstatic --noinput)
#RUN (cd /server/ && python manage.py migrate --noinput)


EXPOSE 80
EXPOSE 8000
EXPOSE 8001
cmd ["supervisord", "-n"]