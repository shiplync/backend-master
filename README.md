# Install locally

1. Clone this repo

1. Install postgresql.
	- On mac, download and install the `postgres app` (easy). 
	- On all other platforms you have to manually install postgis after installing postgres (hard). 

1. Install postgis
	- `brew install postgis`

1. Initialize database for postgis support:

	Create a database and run `CREATE EXTENSION POSTGIS;` followed by `CREATE EXTENSION POSTGIS_TOPOLOGY;`
	
1. Install and setup RabbitMQ
	- Create rabbitmq user: `sudo rabbitmqctl add_user name password`
	- Start rabbitMQ: `sudo rabbitmq-server`

1. Install Virtualenvwrapper using this tutorial: http://docs.python-guide.org/en/latest/dev/virtualenvs/ Then create a virtualenv and set appropiate environment variables in `postactivate`. AWS variables not needed to run the development enviromnemt. Currently S3 is the only service we use and is just used for file transfer. 
	```bash
	# Can take on the following values: 
	impaqd_server.settings.development 
	# impaqd_server.settings.production
	export DJANGO_SETTINGS_MODULE=impaqd_server.settings.development

	# Points to the database
	export DATABASE_URL="postgis://user:password@localhost/traansmission-database"
	
	# Points to local portal. Portal doesn't have to be running
	export PORTAL_URL="http://localhost:9000/#/"

	# Set to your email for testing purposes
	export NOTIFICATION_EMAIL=you@email.com

	# Your host 
	export HOST="http://localhost:8000"
 	
	#Points to rabbitmq server
 	export CELERY_BROKER_URL="amqp://user:password@localhost:5672//"

 	# Some value
 	export SECRET_KEY="1234567"

 	# Version of postgis. 
 	# Examples: 
 	# 2.1 is "2 1"
 	# 2.1.2 is "2 1 2"
	export POSTGIS_VERSION="2 1"
	
	# S3 bucket prefix. that should be something unique associated with you
	# e.g. local-john. Make sure NOT use traansmission, traansmission-sandbox or traansmission-demo
	export S3_BUCKET_PREFIX="local-john"
	
	# AWS Access keys (used to connect to S3)
	export AWS_ACCESS_KEY_ID="your_key_id"
	export AWS_SECRET_ACCESS_KEY="your_secret_access_key"
	
	# Our current Terms of Service version
	export TOS_CURRENT_VERSION=1
	```

1. Install requirements `pip install -r <requirements-file>`. For development, the <requirements-file> is requirements/development.txt

1. If running rabbitmq locally, add rabbitmq user (optional) and start server.
	- Create rabbitmq user: `sudo rabbitmqctl add_user name password`
	- Start rabbitMQ: `sudo rabbitmq-server`

1. Syncronize and migrate database:
	```sh
	$ ./manage.py syncdb
	$ ./manage.py migrate
	```

1. Start Django server: `./manage.py runserver`

1. Start celery server: `celery -A impaqd_server worker -l info`

1. Create a Django admin user

1. Login to Django admin and save the Global Settings object once (Necessary after ininializing the database for the first time).

### Test worker
A fast way to check if the web server is connected to the worker is to run `curl -X GET -H "Content-Type: application/json" http://productionordemohost/api/tests/worker_test/`. A successful response will look like this: `{"success": true}`
