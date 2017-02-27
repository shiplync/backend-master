from ubuntu:14.04
MAINTAINER Emil Lamm Nielsen

# keep upstart quiet
RUN dpkg-divert --local --rename --add /sbin/initctl
RUN ln -sf /bin/true /sbin/initctl

# no tty
ENV DEBIAN_FRONTEND noninteractive

# get up to date
RUN apt-get update --fix-missing

# global installs [applies to all envs!]
RUN apt-get install -y build-essential git libpq-dev
RUN apt-get install -y python python-dev python-setuptools
RUN apt-get install -y python-pip python-virtualenv
RUN apt-get install -y nginx supervisor
RUN apt-get install -y binutils libpq-dev libproj-dev gdal-bin

# stop supervisor service as we'll run it manually
RUN service supervisor stop

RUN pip install supervisor-stdout

# create a virtual environment and install all depsendecies from pypi
RUN virtualenv /opt/venv
ADD requirements/common.txt /opt/venv/requirements/common.txt
ADD requirements/development.txt /opt/venv/requirements/development.txt
ADD requirements/production.txt /opt/venv/requirements/production.txt
RUN /opt/venv/bin/pip install -r /opt/venv/requirements/production.txt

EXPOSE 8000
EXPOSE 5672


ENV PYTHONPATH /opt/app:$PYTHONPATH
ENV DJANGO_SETTINGS_MODULE impaqd_server.settings.production
ENV TOS_CURRENT_VERSION 1
ENV DEBUG false

ADD ./supervisord.conf /etc/supervisord.conf
ADD ./nginx.conf /etc/nginx/nginx.conf

# restart nginx to load the config
RUN service nginx stop

# deploy code
ADD . /opt/app

RUN /opt/venv/bin/python /opt/app/manage.py collectstatic --noinput

#CMD /opt/venv/bin/gunicorn -b :8000 impaqd_server.wsgi
#CMD ["nginx"]

COPY ./docker-entrypoint.sh /opt
ENTRYPOINT ["/opt/docker-entrypoint.sh"]