#!/bin/bash

finish() {
    if [ $# -ne 0 ]; then
        exec $@
    fi

    exit 0
}

manageDb() {
    . /opt/rssgenerator-env/bin/activate

    pushd /opt/django_rssgenerator
    python manage.py migrate

    chown www-data:www-data /opt/rssgenerator-data/rssgenerator.sqlite3
    deactivate
}

if [ $# -ne 0 ]; then
    option=$1
    shift
fi

if [ ! -e /opt/rssgenerator-data/rssgenerator.sqlite3 ]; then
    manageDb

    . /opt/rssgenerator-env/bin/activate
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
    deactivate

    chown -R www-data:www-data /opt/rssgenerator-data
    finish
fi

case "${option}" in
    "update")
        manageDb
        unset option
        ;;
esac

finish ${option} $@
