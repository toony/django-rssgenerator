#!/bin/bash

finish() {
    if [ $# -ne 0 ]; then
        exec $@
    fi
}

logFile() {
    touch /var/log/django.log
    chown www-data:www-data /var/log/django.log

    [ ! -e /var/log/nginx ] && mkdir -p /var/log/nginx
    [ ! -e /var/log/supervisor ] && mkdir -p /var/log/supervisor
}

manageDb() {
    . /opt/rssgenerator-env/bin/activate

    pushd /opt/django_rssgenerator
    python manage.py migrate

    chown www-data:www-data /opt/rssgenerator-data/rssgenerator.sqlite3
    deactivate
}

setUpAllowedHosts() {
    if [ -z "${ALLOWED_HOSTS}" ]; then
        ALLOWED_HOSTS='*'
    fi
    echo ${ALLOWED_HOSTS}
    
    sed -i -e "s#^\(ALLOWED_HOSTS =.\+$\)#ALLOWED_HOSTS = ['${ALLOWED_HOSTS}']#" /opt/django_rssgenerator/django_rssgenerator/settings.py
}

mode=upgrade
if [ ! -e /opt/rssgenerator-data/rssgenerator.sqlite3 ]; then
    mode=install
fi

logFile
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
