========================
alltime_athletics_python
========================
Scrapes Peter Larsson's website `Alltime Athletics`_.
Check out `my blog`_ to see how this data can be visualized.

Just give me the data
-------
The latest data frame can be found `here as a csv`_, or  here_ in parquet_ format.

Here are women's world record performances.

+----+------------------------+---------------------------+----------+
|    | event                  | name                      | result   |
+====+========================+===========================+==========+
|  0 | 100 metres             | Florence Griffith-Joyner  | 10.49    |
+----+------------------------+---------------------------+----------+
|  1 | 100m/110m hurdles      | Oluwatobiloba Amusan      | 12.12    |
+----+------------------------+---------------------------+----------+
|  2 | 200 metres             | Florence Griffith-Joyner  | 21.34    |
+----+------------------------+---------------------------+----------+
|  3 | 400 metres             | Marita Koch               | 47.60    |
+----+------------------------+---------------------------+----------+
|  4 | 400m hurdles           | Sydney McLaughlin-Levrone | 50.68    |
+----+------------------------+---------------------------+----------+
|  5 | 800 metres             | Jarmila Kratochvílová     | 1:53.28  |
+----+------------------------+---------------------------+----------+
|  6 | 1500 metres            | Faith Kipyegon            | 3:49.11  |
+----+------------------------+---------------------------+----------+
|  7 | 1 Mile                 | Sifan Hassan              | 4:12.33  |
+----+------------------------+---------------------------+----------+
|  8 | 3000 metres            | Wang Junxia               | 8:06.11  |
+----+------------------------+---------------------------+----------+
|  9 | 3000m steeplechase     | Beatrice Chepkoech        | 8:44.32  |
+----+------------------------+---------------------------+----------+
| 10 | 5000 metres            | Faith Kipyegon            | 14:05.20 |
+----+------------------------+---------------------------+----------+
| 11 | 10000 metres           | Letesenbet Gidey          | 29:01.03 |
+----+------------------------+---------------------------+----------+
| 12 | 20 km race walk        | Yelena Lashmanova         | 1:23:39  |
+----+------------------------+---------------------------+----------+
| 13 | half-marathon          | Letesenbet Gidey          | 62:52    |
+----+------------------------+---------------------------+----------+
| 14 | marathon               | Brigid Kosgei             | 2:14:04  |
+----+------------------------+---------------------------+----------+
| 15 | 50 km race walk        | Yelena Lashmanova         | 3:50:42  |
+----+------------------------+---------------------------+----------+
| 16 | 60 metres              | Irina Privalova           | 6.92     |
+----+------------------------+---------------------------+----------+
| 17 | 60 metres              | Irina Privalova           | 6.92     |
+----+------------------------+---------------------------+----------+
| 18 | 300 metres             | Shaunae Miller-Uibo       | 34.41    |
+----+------------------------+---------------------------+----------+
| 19 | 1000 metres            | Svetlana Masterkova       | 2:28.98  |
+----+------------------------+---------------------------+----------+
| 20 | 2000 metres            | Francine Niyonsaba        | 5:21.56  |
+----+------------------------+---------------------------+----------+
| 21 | 2000m steeplechase     | Gesa Felicitas Krause     | 5:52.80  |
+----+------------------------+---------------------------+----------+
| 22 | 2 Miles                | Meseret Defar             | 8:58.58  |
+----+------------------------+---------------------------+----------+
| 23 | 5000 metres track walk | Gillian O'Sullivan        | 20:02.60 |
+----+------------------------+---------------------------+----------+
| 24 | 10 km race walk        | Yelena Nikolayeva         | 41:04    |
+----+------------------------+---------------------------+----------+
| 25 | 10km road              | Yalemzerf Yehualaw        | 29:14    |
+----+------------------------+---------------------------+----------+
| 26 | 15km road              | Letesenbet Gidey          | 44:20    |
+----+------------------------+---------------------------+----------+
| 27 | 20km road              | Letesenbet Gidey          | 59:46+   |
+----+------------------------+---------------------------+----------+
| 28 | 30km road              | Ruth Chepngetich          | 1:34:01+ |
+----+------------------------+---------------------------+----------+


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

..  _`my blog`:  https://camminady.org/posts/world-records/world_records.html
..  _`here as a csv`: https://github.com/thomascamminady/alltime_athletics_python/blob/main/dataframes/alltime_athletics_version_2023-06-12.csv
..  _`Alltime Athletics`: http://www.alltime-athletics.com
..  _parquet: https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html
..  _here: https://github.com/thomascamminady/alltime_athletics_python/blob/main/dataframes/alltime_athletics_version_2023-06-12.parquet
..  _PyPI: https://pypi.org/project/alltime-athletics-python/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`thomascamminady/cookiecutter-pypackage`: https://github.com/thomascamminady/cookiecutter-pypackage
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
