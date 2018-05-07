FROM debian:jessie
MAINTAINER Anthony Prades <toony.github@chezouam.net>

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -yq \
    --no-install-recommends \
    python \
    virtualenv \
    nginx \
    supervisor \
    libmagic1 \
    python-dev \
    python-setuptools \
    build-essential \
    python-tk \
    libjpeg-dev \
    zlib1g-dev \
    tcl8.6-dev \
    tk8.6-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    && apt-get clean \
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

RUN cd /opt \
    && mkdir -p rssgenerator-data \
    && virtualenv rssgenerator-env \
    && mkdir -p /opt/rssgenerator-env/var \
    && . /opt/rssgenerator-env/bin/activate \
    && cd /opt/rssgenerator-src \
    && python setup.py sdist \
    && cd dist \
    && pip install django-rssgenerator-0.13.tar.gz \
    && pip install gunicorn \
    && cd /opt \
    && django-admin.py startproject django_rssgenerator \
    && cd /opt/django_rssgenerator/django_rssgenerator \
    && sed -i -e "s/\(INSTALLED_APPS =.\+$\)/\1\n    'rssgenerator',\n    'background_task',/" settings.py \
    && sed -i -e "s#^\(TIME_ZONE =.\+$\)#TIME_ZONE = 'Europe/Paris'#" settings.py \
    && sed -i -e "s#^\(.\+'NAME': \).\+db.sqlite3.\+\$#\1'/opt/rssgenerator-data/rssgenerator.sqlite3'#" settings.py \
    && echo "RSSGENERATOR_LOCAL_DATA = '/opt/rssgenerator-data/localData'" >> settings.py \
    && echo 'ADMINS = (' >> settings.py \
    && echo "('Anthony Prades', 'toony.github@chezouam.net')," >> settings.py \
    && echo ')' >> settings.py \
    && echo '' >> settings.py \
    && echo 'MANAGERS = ADMINS' >> settings.py \
    && echo "STATIC_ROOT = '/opt/rssgenerator-static'" >> settings.py \
    && cd /opt/django_rssgenerator \
    && python manage.py collectstatic --noinput \
    && cd /opt/django_rssgenerator \
    && rm -rf /opt/rssgenerator-src \
    && chown -R www-data:www-data /opt/rssgenerator-data

RUN DEBIAN_FRONTEND=noninteractive apt-get remove --purge -yq \
    python-dev \
    python-setuptools \
    build-essential \
    python-tk \
    libjpeg-dev \
    zlib1g-dev \
    tcl8.6-dev \
    tk8.6-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    && apt-get autoremove --purge -yq

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
