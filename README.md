# django-rssgenerator

A very simple RSS generator created for my personal needs

## Developer environment

Build it using:
```
git clone https://github.com/toony/django-rssgenerator.git django-rssgenerator
cd django-rssgenerator
./buildDevEnv.sh
```

Then, connect to: http://127.0.0.1:8000/admin

Default admin account: admin/admin

To run async tasks:
```
cd /path/to/django-rssgenerator/git/../rssgenerator-env/project
. ../rssgenerator-env/bin/activate
python manage.py process_tasks
```

If you stop development server, you may start it without rebuild all developer environment:
```
cd /path/to/django-rssgenerator/git/../rssgenerator-env/project
python manage.py runserver
```

## Docker
Build docker container using: 
```
docker build -t toony/rssgenerator .
docker run -d toony/rssgenerator
```

Then, connect to: `http://<container ip>/admin`

Default admin account: admin/admin

### Configuring ALLOWED_HOSTS
```
docker run -e 'ALLOWED_HOSTS=[IP|FQDN]' -d toony/rssgenerator
```
