#!/bin/bash
#/opt/venv/bin/python /opt/app/manage.py migrate                  # Apply database migrations
#/opt/venv/bin/python /opt/app/manage.py collectstatic --noinput  # Collect static files
if [ "$IS_WORKER" == "true" ]; then
	echo 'starting celery worker';
	export C_FORCE_ROOT=1
	/opt/venv/bin/celery -A impaqd_server worker -l info -B -s /opt/celerybeat-schedule
else
	echo 'starting gunicorn web server';
	#/opt/venv/bin/gunicorn -b :8000 impaqd_server.wsgi
	supervisord -c /etc/supervisord.conf -n
fi