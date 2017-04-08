#!/bin/bash

which virtualenv > /dev/null 2>&1
if [ $? -ne 0 ]; then
	echo "virtualenv must be installed and accessible from PATH"
	exit 1
fi

WORKSPACE=`dirname $0`
pushd ${WORKSPACE}
WORKSPACE=`pwd`
GIT_CLONE=`basename ${WORKSPACE}`

PYENV="../rssgenerator-env"
mkdir -p ${PYENV}
pushd ${PYENV}

# Create and activate virtualenv
virtualenv rssgenerator-env
. ./rssgenerator-env/bin/activate

# Install dependencies
pip install Django==1.8 PyRSS2Gen python-magic

# Initialize Django project
django-admin startproject project

popd
cp "docker/djangoProjet-urls.py" ${PYENV}"/project/project/urls.py"

pushd ${PYENV}"/project"
ln -s "../../"${GIT_CLONE}"/rssgenerator" .

pushd project
sed -i -e "s/\(INSTALLED_APPS =.\+$\)/\1\n    'rssgenerator',/" settings.py
popd

python manage.py migrate

echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
echo "Administrator account: admin/admin"

exec python manage.py runserver

