# destroy, create, and run test database and API
# deactivate any old environment
# activate python environment
. venv/bin/activate
# clear old data
./manage.py flush --settings=impaqd_server.settings.protractor
# add tables
./manage.py syncdb  --settings=impaqd_server.settings.protractor
# add migrations
./manage.py migrate --settings=impaqd_server.settings.protractor
# run any test setup
 ./manage.py shell --settings=impaqd_server.settings.protractor < scripts/protractor_setup.py
# run the server
./manage.py runserver  --settings=impaqd_server.settings.protractor
