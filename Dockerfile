FROM debian:bullseye
MAINTAINER Anthony Prades <toony.github@chezouam.net>

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -yq \
    --no-install-recommends \
    python3 \
    python3-venv \
    nginx \
    supervisor \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /etc/rssgenerator
COPY docker/gunicorn_config.py /etc/rssgenerator/gunicorn_config.py

RUN mkdir -p /opt/rssgenerator-src
COPY rssgenerator /opt/rssgenerator-src/rssgenerator
COPY setup.py /opt/rssgenerator-src/setup.py
COPY README.md /opt/rssgenerator-src/README.md
COPY README.txt /opt/rssgenerator-src/README.txt
COPY MANIFEST.in /opt/rssgenerator-src/MANIFEST.in
COPY LICENSE /opt/rssgenerator-src/LICENSE
COPY docker/configSettings.py /tmp/configSettings.py

RUN cd /opt \
    && mkdir -p rssgenerator-data \
    && python3 -m venv rssgenerator-env \
    && mkdir -p /opt/rssgenerator-env/var \
    && . /opt/rssgenerator-env/bin/activate \
    && pip install -U pip wheel \
    && pip install gunicorn \
    && cd /opt/rssgenerator-src \
    && python3 setup.py sdist \
    && cd dist \
    && pip install django-rssgenerator-1.11.tar.gz \
    && cd /opt \
    && django-admin.py startproject django_rssgenerator \
    && cd /opt/django_rssgenerator/django_rssgenerator \
    && sed -i -e "s#^\(DEBUG =.\+$\)#DEBUG = False#" settings.py \
    && sed -i -e "s/\(INSTALLED_APPS =.\+$\)/\1\n    'rssgenerator',\n    'background_task',/" settings.py \
    && sed -i -e "s#^\(TIME_ZONE =.\+$\)#TIME_ZONE = 'Europe/Paris'#" settings.py \
    && sed -i -e "s#^\(.\+'NAME': \).\+db.sqlite3.\+\$#\1'/opt/rssgenerator-data/rssgenerator.sqlite3'#" settings.py \
    && cat /tmp/configSettings.py >> settings.py \
    && rm /tmp/configSettings.py \
    && cd /opt/django_rssgenerator \
    && python3 manage.py collectstatic --noinput \
    && cd /opt/django_rssgenerator \
    && rm -rf /opt/rssgenerator-src \
    && chown -R www-data:www-data /opt/rssgenerator-data

RUN DEBIAN_FRONTEND=noninteractive apt-get remove --purge -yq \
    && apt-get autoremove --purge -yq \
    && apt-get clean

COPY docker/djangoProjet-urls.py /opt/django_rssgenerator/django_rssgenerator/urls.py

ADD docker/rssgenerator.nginx /etc/nginx/sites-available/rssgenerator
RUN rm -f /etc/nginx/sites-enabled/default
RUN ln -s /etc/nginx/sites-available/rssgenerator /etc/nginx/sites-enabled/rssgenerator
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

RUN sed -i -e 's/^\(\[supervisord\]\)$/\1\nnodaemon=true/' /etc/supervisor/supervisord.conf
COPY docker/supervisor.conf /etc/supervisor/conf.d/rssgenerator.conf

COPY docker/init-rssgenerator.sh /init-rssgenerator.sh
RUN chmod +x /init-rssgenerator.sh

COPY docker/processAsyncTasks.sh /processAsyncTasks.sh
RUN chmod +x /processAsyncTasks.sh
 
EXPOSE 80

ENTRYPOINT ["/init-rssgenerator.sh"]
CMD ["/usr/bin/supervisord"]
