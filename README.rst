========================
alltime_athletics_python
========================
Scrapes http://www.alltime-athletics.com


Run
-------
Download all data via ````
.. code-block:: bash

   poetry run python alltime_athletics_python/main.py parse "./data"


To read the processed data, run

.. code-block:: python

   from alltime_athletics_python.io import import_running_only_events
   df = import_running_only_events()


Development
--------
To set up the project, simply run

.. code-block:: bash

   make init





Credits
-------

This package was created with Cookiecutter_ and `thomascamminady/cookiecutter-pypackage`_, a fork of the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`thomascamminady/cookiecutter-pypackage`: https://github.com/thomascamminady/cookiecutter-pypackage
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
