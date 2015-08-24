# django-rssgenerator

A very simple RSS generator created for my personal needs

## Developer environment

Build it using:
```
git clone https://github.com/toony/django-rssgenerator.git django-rssgenerator
cd django-rssgenerator
./buildDevEnv.sh
```

Then, connect to: http://127.0.0.1:8000/

Default admin account: admin/admin

## Docker
Build docker container using: 
```
docker build -t toony/rssgenerator .
docker run -d toony/rssgenerator
```

Then, connect to: `http://<container ip>/admin`

Default admin account: admin/admin
