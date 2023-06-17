========================
alltime_athletics_python
========================
Scrapes Peter Larsson's website `Alltime Athletics`_.
Check out `my blog`_ to see how this data can be visualized.

Just give me the data
-------
The latest data frame can be found `here as a csv`_, or  here_ in parquet_ format. Or run

.. code-block:: python

   import pandas as pd

   df = pd.read_csv(
        "https://media.githubusercontent.com/media/thomascamminady/alltime_athletics_python/main/dataframes/latest_version_alltime_athletics.csv"
   )




As an example, here are the women's world record performances, sorted by the date of the world record.



+----+------------------------+---------------------------+----------+-----------------+
|    | event                  | name                      | result   | date of event   |
+====+========================+===========================+==========+=================+
|  0 | 800 metres             | Jarmila Kratochvílová     | 1:53.28  | 1983-07-26      |
+----+------------------------+---------------------------+----------+-----------------+
|  1 | 400 metres             | Marita Koch               | 47.60    | 1985-10-06      |
+----+------------------------+---------------------------+----------+-----------------+
|  2 | 100 metres             | Florence Griffith-Joyner  | 10.49    | 1988-07-16      |
+----+------------------------+---------------------------+----------+-----------------+
|  3 | 200 metres             | Florence Griffith-Joyner  | 21.34    | 1988-09-29      |
+----+------------------------+---------------------------+----------+-----------------+
|  4 | 60 metres              | Irina Privalova           | 6.92     | 1993-02-11      |
+----+------------------------+---------------------------+----------+-----------------+
|  5 | 3000 metres            | Wang Junxia               | 8:06.11  | 1993-09-13      |
+----+------------------------+---------------------------+----------+-----------------+
|  6 | 60 metres              | Irina Privalova           | 6.92     | 1995-02-09      |
+----+------------------------+---------------------------+----------+-----------------+
|  7 | 10 km race walk        | Yelena Nikolayeva         | 41:04    | 1996-04-20      |
+----+------------------------+---------------------------+----------+-----------------+
|  8 | 1000 metres            | Svetlana Masterkova       | 2:28.98  | 1996-08-23      |
+----+------------------------+---------------------------+----------+-----------------+
|  9 | 5000 metres track walk | Gillian O'Sullivan        | 20:02.60 | 2002-07-14      |
+----+------------------------+---------------------------+----------+-----------------+
| 10 | 2 Miles                | Meseret Defar             | 8:58.58  | 2007-09-14      |
+----+------------------------+---------------------------+----------+-----------------+
| 11 | 20 km race walk        | Yelena Lashmanova         | 1:23:39  | 2018-06-09      |
+----+------------------------+---------------------------+----------+-----------------+
| 12 | 3000m steeplechase     | Beatrice Chepkoech        | 8:44.32  | 2018-07-20      |
+----+------------------------+---------------------------+----------+-----------------+
| 13 | 300 metres             | Shaunae Miller-Uibo       | 34.41    | 2019-06-20      |
+----+------------------------+---------------------------+----------+-----------------+
| 14 | 1 Mile                 | Sifan Hassan              | 4:12.33  | 2019-07-12      |
+----+------------------------+---------------------------+----------+-----------------+
| 15 | 2000m steeplechase     | Gesa Felicitas Krause     | 5:52.80  | 2019-09-01      |
+----+------------------------+---------------------------+----------+-----------------+
| 16 | marathon               | Brigid Kosgei             | 2:14:04  | 2019-10-13      |
+----+------------------------+---------------------------+----------+-----------------+
| 17 | 15km road              | Letesenbet Gidey          | 44:20    | 2019-11-17      |
+----+------------------------+---------------------------+----------+-----------------+
| 18 | 50 km race walk        | Yelena Lashmanova         | 3:50:42  | 2020-09-05      |
+----+------------------------+---------------------------+----------+-----------------+
| 19 | 10000 metres           | Letesenbet Gidey          | 29:01.03 | 2021-06-08      |
+----+------------------------+---------------------------+----------+-----------------+
| 20 | 2000 metres            | Francine Niyonsaba        | 5:21.56  | 2021-09-14      |
+----+------------------------+---------------------------+----------+-----------------+
| 21 | half-marathon          | Letesenbet Gidey          | 62:52    | 2021-10-24      |
+----+------------------------+---------------------------+----------+-----------------+
| 22 | 20km road              | Letesenbet Gidey          | 59:46+   | 2021-10-24      |
+----+------------------------+---------------------------+----------+-----------------+
| 23 | 10km road              | Yalemzerf Yehualaw        | 29:14    | 2022-02-27      |
+----+------------------------+---------------------------+----------+-----------------+
| 24 | 400m hurdles           | Sydney McLaughlin-Levrone | 50.68    | 2022-07-22      |
+----+------------------------+---------------------------+----------+-----------------+
| 25 | 100m/110m hurdles      | Oluwatobiloba Amusan      | 12.12    | 2022-07-24      |
+----+------------------------+---------------------------+----------+-----------------+
| 26 | 30km road              | Ruth Chepngetich          | 1:34:01+ | 2022-10-09      |
+----+------------------------+---------------------------+----------+-----------------+
| 27 | 1500 metres            | Faith Kipyegon            | 3:49.11  | 2023-06-02      |
+----+------------------------+---------------------------+----------+-----------------+
| 28 | 5000 metres            | Faith Kipyegon            | 14:05.20 | 2023-06-09      |
+----+------------------------+---------------------------+----------+-----------------+


You would get this table by using ``polars`` and running

.. code-block:: python

   import polars as pl

   df = pl.read_csv(
        "https://media.githubusercontent.com/media/thomascamminady/alltime_athletics_python/main/dataframes/latest_version_alltime_athletics.csv"
   )

   (
    df.filter(pl.col("rank") == 1)
    .filter(pl.col("sex") == "female")
    .select("event", "name", "result", "date of event")
    .sort("date of event")
   )


Download
-------
If you have cloned the source code, you can run

.. code-block:: python

   etry run python alltime_athletics_python/app.py


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
..  _`here as a csv`: https://github.com/thomascamminady/alltime_athletics_python/blob/main/dataframes/latest_version_alltime_athletics.csv
..  _`Alltime Athletics`: http://www.alltime-athletics.com
..  _parquet: https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html
..  _here: https://github.com/thomascamminady/alltime_athletics_python/blob/main/dataframes/latest_version_alltime_athletics.parquet
..  _PyPI: https://pypi.org/project/alltime-athletics-python/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`thomascamminady/cookiecutter-pypackage`: https://github.com/thomascamminady/cookiecutter-pypackage
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
