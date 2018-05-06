#!/bin/bash

. /opt/rssgenerator-env/bin/activate

pushd /opt/django_rssgenerator
exec python manage.py process_tasks
