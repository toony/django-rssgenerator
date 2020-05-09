#!/bin/bash

# Check python version
for pythonbin in python python3; do
    ${pythonbin} -c 'import sys; exit(1) if sys.version_info.major < 3 or sys.version_info.minor < 5 else exit(0)'
    if [ $? -eq 0 ]; then
        PYTHONBIN=${pythonbin}
        break
    fi
done

if [ -z "${PYTHONBIN}" ]; then
    echo "Python 3.5+ needed!" 1>&2
    exit 1
fi

WORKSPACE=`dirname $0`
pushd ${WORKSPACE} > /dev/null 2>&1
WORKSPACE=`pwd`
GIT_CLONE=`basename ${WORKSPACE}`
pushd .. > /dev/null 2>&1
WORKSPACE=`pwd`
GIT_CLONE=${WORKSPACE}"/"${GIT_CLONE}

DJANGOENV=${WORKSPACE}"/rssgenerator-djangoenv"
mkdir -p ${DJANGOENV}

# Create and activate virtualenv
pushd ${DJANGOENV} > /dev/null 2>&1
${PYTHONBIN} -m venv rssgenerator-env
. ./rssgenerator-env/bin/activate

# Install dependencies
pip install wheel
pip install 'Django==2.2.12' 'PyRSS2Gen' 'python-magic' 'django-background-tasks==1.2.5' 'pillow>=5.1.0'

# Initialize Django project
django-admin startproject project

popd > /dev/null 2>&1
cp ${GIT_CLONE}"/docker/djangoProjet-urls.py" ${DJANGOENV}"/project/project/urls.py"

pushd ${DJANGOENV}"/project" > /dev/null 2>&1
ln -s ${GIT_CLONE}"/rssgenerator" .

pushd project > /dev/null 2>&1
sed -i -e "s/\(INSTALLED_APPS =.\+$\)/\1\n    'rssgenerator',\n    'background_task',/" settings.py
cat >> settings.py <<EOF
RSSGENERATOR_LOCAL_DATA = '${WORKSPACE}/localData'
STATIC_ROOT = '${WORKSPACE}/rssgenerator-static'

# Use only TemporaryFileUploadHandler for uploaded files
FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)
EOF
popd > /dev/null 2>&1

python manage.py migrate

echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
echo "Administrator account: admin/admin"

exec python manage.py runserver

