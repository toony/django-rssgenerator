#!/bin/bash

finish() {
    if [ $# -ne 0 ]; then
        exec $@
    fi
}

manageDb() {
    . /opt/rssgenerator-env/bin/activate

    pushd /opt/django_rssgenerator
    python manage.py migrate

    chown www-data:www-data /opt/rssgenerator-data/rssgenerator.sqlite3
    deactivate
}

mode=upgrade
if [ ! -e /opt/rssgenerator-data/rssgenerator.sqlite3 ]; then
    mode=install
fi

manageDb

if [ ${mode} == 'install' ]; then    
    . /opt/rssgenerator-env/bin/activate
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
    deactivate

    chown -R www-data:www-data /opt/rssgenerator-data
    finish
fi

finish ${option} $@
