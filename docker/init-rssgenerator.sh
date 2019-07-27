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

setUpAllowedHosts() {
    echo "opop"
    if [ -z "${ALLOWED_HOSTS}" ]; then
        echo "opop"
        ALLOWED_HOSTS='*'
    fi
    echo ${ALLOWED_HOSTS}
    
    sed -i -e "s#^\(ALLOWED_HOSTS =.\+$\)#ALLOWED_HOSTS = ['${ALLOWED_HOSTS}']#" /opt/django_rssgenerator/django_rssgenerator/settings.py
}

mode=upgrade
if [ ! -e /opt/rssgenerator-data/rssgenerator.sqlite3 ]; then
    mode=install
fi

setUpAllowedHosts
manageDb

if [ ${mode} == 'install' ]; then    
    . /opt/rssgenerator-env/bin/activate
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
    deactivate

    chown -R www-data:www-data /opt/rssgenerator-data
    finish
fi

finish ${option} $@
