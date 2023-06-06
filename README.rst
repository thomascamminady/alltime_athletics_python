========================
alltime_athletics_python
========================
Scrapes Peter Larsson's website `Alltime Athletics`_.

Just give me the data
-------
The latest data frame (in parquet_ format) can be found here_.


Download
-------

If you installed this package from PyPI_, run

.. code-block:: python

   from alltime_athletics_python.io import download_data
   download_data()

Note that ``download_data()`` reads data from Alltime Athletics **AS IS**. You will definitely need to do some postprocessing.

Postprocessing
-------

To read the processed data, run

.. code-block:: python

   from alltime_athletics_python.io import import_running_only_events
   df = import_running_only_events("./data")


Development
--------
To set up the project, simply run

.. code-block:: bash

   make init





Credits
-------

This tool does not take credit for the amazing effort by Peter Larsson, who compiles `Alltime Athletics`_. Alltime Athletics is an amazing collection of track and field results with a lot of work that must have gone into it. Thank you, Peter Larsson.

The only functionality that this tool provides is to have an easier way to read data from Alltime Athletics.


This package was created with Cookiecutter_ and `thomascamminady/cookiecutter-pypackage`_, a fork of the `audreyr/cookiecutter-pypackage`_ project template.


..  _`Alltime Athletics`: http://www.alltime-athletics.com
..  _parquet: https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html
..  _here: https://github.com/thomascamminady/alltime_athletics_python/blob/main/dataframes/alltime_athletics_version_2023-06-06.parquet
..  _PyPI: https://pypi.org/project/alltime-athletics-python/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`thomascamminady/cookiecutter-pypackage`: https://github.com/thomascamminady/cookiecutter-pypackage
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
