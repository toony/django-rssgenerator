# django-rssgenerator

A very simple RSS generator created for my personal needs

## Developer environment

Build it using:
```
git clone https://github.com/toony/django-rssgenerator.git django-rssgenerator
cd django-rssgenerator
./buildDevEnv.sh
```

## Docker
Build docker container using: 
```
docker build -t toony/rssgenerator .
docker run -d toony/rssgenerator
```

Then connect to: `http://<container ip>/admin`

Default admin account: admin/admin
