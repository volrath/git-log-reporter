==================
 Git Log Reporter
==================

Small web service built with `Flask`_ that gives a log report of
requested repositories. This web service responds to ``POST`` requests
using ``Content-Type: application/json``.

**Disclaimer:** This is still beta. I'd recommend being careful if
it's used in production.


Installation and basic usage
============================

After cloning this repo you need to edit ``GIT_REPOS_PATH`` in
``app.py`` specifying the root directory where your repositories are,
for example: ``/var/repositories``.

Right after that you can run the project::

    pip install -r requirements.pip  # Right now it only depends on Flask, so you can just install it.
    python app.py

Then you can query the service with ``curl`` (or whatever)::

    curl -X POST -H 'Content-Type: application/json' -d '{"repos": ["myproject"], "options": {"author": "Daniel Barreto", "since": "1 day ago"}}' http://localhost:5000/

The only required argument in the data passed to the web service is
"repos" which needs to be a list of repository names existing on the
``GIT_REPOS_PATH``.

The "options" option can have any verbose option that ``git log``
accepts. If the option does not (or is not required to) accept a value
(for example ``--merges``), you can pass ``null`` as it value.


Deployment and possible caveats
===============================

Exposing this information to everyone using an open web server can be
a risk for you, so you might want to only allow certain IP addresses
to access the application. An example on how to do this using `Nginx`_
and `gunicorn`_ can be found in ``nginx.conf.example``.

Another thing to keep in mind is that the user running the application
needs to be able to access your ``GIT_REPOS_PATH`` and every repo
you'd want a report of.

.. _Flask: http://flask.pocoo.org/
.. _Nginx: http://wiki.nginx.org/
.. _gunicorn: http://gunicorn.org/
