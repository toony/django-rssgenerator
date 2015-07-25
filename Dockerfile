FROM debian:jessie
MAINTAINER Anthony Prades <toony.github@chezouam.net>

RUN apt-get update \
    && apt-get upgrade -yq \
    && DEBIAN_FRONTEND=noninteractive apt-get install -yq \
	--no-install-recommends \
    python \
    virtualenv \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /etc/rssgenerator
COPY docker/gunicorn_config.py /etc/rssgenerator/gunicorn_config.py

COPY docker/init-rssgenerator.sh /init-rssgenerator.sh
RUN chmod +x /init-rssgenerator.sh

RUN sed -i -e 's/^\(\[supervisord\]\)$/\1\nnodaemon=true/' /etc/supervisor/supervisord.conf
COPY docker/supervisor.conf /etc/supervisor/conf.d/rssgenerator.conf

ADD docker/rssgenerator.nginx /etc/nginx/sites-available/rssgenerator
RUN rm -f /etc/nginx/sites-enabled/default
RUN ln -s /etc/nginx/sites-available/rssgenerator /etc/nginx/sites-enabled/rssgenerator
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

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
    && pip install django-rssgenerator-0.4.tar.gz \
    && pip install gunicorn \
    && cd /opt \
    && django-admin.py startproject django_rssgenerator \
    && cd /opt/django_rssgenerator/django_rssgenerator \
    && sed -i -e "s/\(INSTALLED_APPS =.\+$\)/\1\n    'rssgenerator',/" settings.py \
    && sed -i -e "s#^\(TIME_ZONE =.\+$\)#TIME_ZONE = 'Europe/Paris'#" settings.py \
    && sed -i -e "s#^\(.\+'NAME': \).\+db.sqlite3.\+\$#\1'/opt/rssgenerator-data/rssgenerator.sqlite3'#" settings.py \
    && sed -i -e "s#^\(]$\)#    url(r'^rssgenerator/', include('rssgenerator.urls', namespace=\"rss\")),\n\1#" urls.py \
    && echo 'ADMINS = (' >> settings.py \
    && echo "('Anthony Prades', 'toony.github@chezouam.net')," >> settings.py \
    && echo ')' >> settings.py \
    && echo '' >> settings.py \
    && echo 'MANAGERS = ADMINS' >> settings.py \
    && cd /opt/django_rssgenerator \
    && rm -rf /opt/rssgenerator-src \
    && chown -R www-data:www-data /opt/rssgenerator-data

VOLUME ["/opt/rssgenerator-data", "/var/log"]
 
EXPOSE 80

ENTRYPOINT ["/init-rssgenerator.sh"]
CMD ["/usr/bin/supervisord"]
