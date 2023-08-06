=============================
acdh-django-filechecker
=============================

Django-App to store, edit, enrich and serialize the results of https://github.com/acdh-oeaw/repo-file-checker


Quickstart
----------

Install acdh-django-filechecker:

    pip install acdh-django-filechecker

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'filechecker',
        ...
    )


Update your project's urls.py:

.. code-block:: python

    urlpatterns = [
        ...
        url(r'^filechecker-rdf/', include('filechecker.fc_arche_urls', namespace='filechecker-rdf')),
        url(r'^filechecker/', include('filechecker.urls', namespace='filechecker')),
        ...
      ]
