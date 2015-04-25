#!/bin/bash

if [ ! -e /opt/rssgenerator-data/rssgenerator.sqlite3 ]; then
    . /opt/rssgenerator-env/bin/activate

    pushd /opt/django_rssgenerator
    python manage.py migrate
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
    deactivate

    chown -R www-data:www-data /opt/rssgenerator-data
fi

exec /usr/bin/supervisord
