#!/bin/bash

which virtualenv > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "virtualenv must be installed and accessible from PATH"
    exit 1
fi

WORKSPACE=`dirname $0`
pushd ${WORKSPACE} > /dev/null 2>&1
WORKSPACE=`pwd`
GIT_CLONE=`basename ${WORKSPACE}`
pushd .. > /dev/null 2>&1
WORKSPACE=`pwd`
GIT_CLONE=${WORKSPACE}"/"${GIT_CLONE}

PYENV=${WORKSPACE}"/rssgenerator-env"
mkdir -p ${PYENV}
pushd ${PYENV} > /dev/null 2>&1

# Create and activate virtualenv
virtualenv rssgenerator-env
. ./rssgenerator-env/bin/activate

# Install dependencies
pip install Django==1.8.19 PyRSS2Gen python-magic django-background-tasks==1.1.13 pillow>=5.1.0

# Initialize Django project
django-admin startproject project

popd
cp ${GIT_CLONE}"/docker/djangoProjet-urls.py" ${PYENV}"/project/project/urls.py"

pushd ${PYENV}"/project" > /dev/null 2>&1
ln -s ${GIT_CLONE}"/rssgenerator" .

pushd project > /dev/null 2>&1
sed -i -e "s/\(INSTALLED_APPS =.\+$\)/\1\n    'rssgenerator',\n    'background_task',/" settings.py
echo "RSSGENERATOR_LOCAL_DATA = '${WORKSPACE}/localData'" >> settings.py
popd

python manage.py migrate

echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
echo "Administrator account: admin/admin"

exec python manage.py runserver

