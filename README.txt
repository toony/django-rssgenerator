============
RssGenerator
============

RssGenerator is a simple Django app to build simple RSS feeds

Quick start
-----------

1. Add "rssgenerator" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'rssgenerator',
      )

2. Include the RssGenerator URLconf in your project urls.py like this::

      url(r'^rssgenerator/', include('rssgenerator.urls', namespace="rss")),

3. Run `python manage.py syncdb` to create the RssGenerator models.

4. Add RSSGENERATOR_LOCAL_DATA to settings.py.
   This is used to store RSS local data and must be writable by app

4. Start the development server and visit http://127.0.0.1:8000/admin/
  to add content to you RSS feed (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/rssgenerator/ to view you RSS feed.
