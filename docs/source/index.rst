Welcome to Data Engineering UTokyo's documentation!
===================================================

A software package developed for the Center of Nuclear Studies (CNS) to join all data sources and analyze the data in
real-time. The package saves a lot of time by providing an easy-to-use interface for interacting with the data and
allows to automatically extract key results from the data via Maximum Likelihood Estimation (MLE) and search algorithms.


Data sources
============

The package can map csv files created by LabView to pandas dataframes in
real-time up to a sampling rate in linear time, providing a quadratic
speedup compared to reloading the data. Examples include data from the
SSD, PMT, Coil, Heater, Gauge, Laser, Ion and CCD camera. One can
process new formats easily, be creating a child class of Recorder and
just overriding the behaviour which has to differ from the default.

Outputs
=======

The output comes in the of recorders and analyses. The recorders
abstract away loading the csv file as pandas dataframe and keeping it up
to date when more data comes in. The analyses take the recorders,
visualize their data, calculate or fit some metrics and store the result
as csv file.

The recorders also come in a flavor that we call parser. Parsers provide
a solution for handling csv file which are to large for pandas. Each
time we evaluate a parser, it provides us with the next chunk of data as
pandas dataframe, without loading the full dataframe at any point in
time.


Impressions
===========

The plot and histogram are visualizations of the SSD data. The peaks and
the background are fitted with an algorithm.


.. image:: ../../docs/impressions/SSDPeaks.png
   :target: https://github.com/romanwixinger/data-engineering-utokyo


.. image:: ../../docs/impressions/SSDSinglePeak.png
   :target: https://github.com/romanwixinger/data-engineering-utokyo

This 2D plot is obtained by Maximum Likelihood Estimation with a
Gaussian model on an image from the CCD camera.

.. image:: ../../docs/impressions/CCD2DGaussian.png
   :target: https://github.com/romanwixinger/data-engineering-utokyo



How to get started
==================

There are two environments in which this package has been tested:

Locally
-------

You can clone the repository to your local computer, load the data to
your computer, and run the code either in a Jupyter notebook or in a
Python file. Checkout notebooks/recorder_demo.ipynb,
notebooks/ssd_analysis_demo.ipynb and main/main.py as reference.

Install the library by navigating into the repo in your CLI and typing

.. code:: bash

   pip install .

When you start Python, then the following imports should work

.. code:: python

   import data_eng_utokyo


Google Colaboratory
-------------------

You create a Google Account, ask for access to the Google Drive folder,
create your own alias of the folder such that you see it in your on
files, start Google Colaboratory and create a new notebook. In this
notebook, you have to make sure that you import your Google Drive
folder. In a first step, you just mount Google Drive.

.. code:: python

   from google.colab import drive
   drive.mount('/content/drive')

   filepath_drive = "/content/drive/.shortcut-targets-by-id/something/some_folder"

Then, you navigate to the Google Drive folder with commands like

.. code:: console

   cd /content/drive/

and

.. code:: console

   ls

The latter will output the files and folders which are located at your
current position. When you have found the place of your folder, you save
it as code like this:

.. code:: python

   filepath_drive = "/content/drive/.shortcut-targets-by-id/something/some_folder"

Next, you navigate to your drive and clone this repository with the
instructions provided on Github. You can use this `Medium
article <https://medium.com/@ashwindesilva/how-to-use-google-colaboratory-to-clone-a-github-repository-e07cf8d3d22b>`__
and this `Medium
article <https://medium.com/analytics-vidhya/how-to-use-google-colab-with-github-via-google-drive-68efb23a42d>`__
as reference. Read them carefully. Here we just describe the most
important steps:

Clone the repo with.

.. code:: console

   !git clone "https://github.com/romanwixinger/data-engineering-utokyo"

Navigate to the repository in the notebook and verify that you are on
the right branch with

.. code:: console

   !git status

This should output that you are on the branch main. Last, we have to
configure origin such that we can push to Github. So go to Github ->
settings -> Developer settings -> Personal access tokens and create a
personal access token for the repository. Store the access token safely,
you cannot see it afterwards. Then you add the remote origin

.. code:: console

   !git remote add <remote-name> https://{git_username}:{git_token}@github.com/{username}/{repository}.git

Use origin as remote-name, romanwixinger as username,
data-engineering-utokyo as repository and your git_username and
git_token. To verify that it worked, check that the following command
outputs two lines:

.. code:: console

   !git remote -v

Now you can start to import functionality from the package as described
in the examples.

Examples
--------

How to use the package to track your own csv files.

.. code:: python

   from data_eng_utokyo.recorders import SSDRecorder

   ssd_recorder = SSDRecorder(filepath="my_filepath.csv")
   df = ssd_recorder.get_table()               # Full table
   metadata_df = ssd_recorder.get_metadata()   # Just metadata

Next we can setup analyses which performs MLE and visualize the data.

.. code:: python

   from data_eng_utokyo.analyses import SSDAnalysis

   ssd_analysis = SSDAnalysis(
     recorder=ssd_recorder,
     image_src="../../plots/",
     image_extension=".png"
   )
   ssd_analysis.run()

Last, we can also use a runner to perform many analyses in real-time
during an experiment.

.. code:: python

   from data_eng_utokyo.utilities import Runner
   from src.analyses import (
        SSDAnalysis,
        PMTAnalysis,
    )

   analyses = [
     SSDAnalysis(recorder=ssd_recorder, image_src="../../plots/mock"),
     PMTAnalysis(recorder=pmt_recorder, image_src="../../plots/mock")
   ]
   runner = Runner(analyses=analyses)
   runner.run(cycles=3*60, period_s=60) # Every 60 seconds for three hours

Sometimes, we want to perform the same analysis on many different files.
Then, we can leverage the FileRecorder to find the filenames, paths and
creation times of these files.

.. code:: python

   from data_eng_utokyo.recorders import FileRecorder

   file_recorder = FileRecorder(
     filepath="path_to_the_folder/",
     match="regex_pattern_to_find_the_right_files"
   )
   file_df = file_recorder.get_table()

From time to time, we want to test our analysis with a recorder that
represents data that we know well. For this purpose, we introduce the
StaticRecorder. This class behaves like a recorder, but its data is a
fixed dataframe given upon initialization.

.. code:: python

   import pandas as pd

   from data_eng_utokyo.recorders import StaticRecorder

   df = pd.DataFrame(
     data=[["Alice", 25], ["Bob", 23], ["Eve", 27]],
     columns=["name", "age"]
     )
   static_recorder = StaticRecorder(df=df)


.. toctree::
   :maxdepth: 4
   :caption: Contents:


**Structure**
=============
.. toctree::
   :maxdepth: 4
   :caption: Data

   data

.. toctree::
   :maxdepth: 4
   :caption: Recorders

   recorders

.. toctree::
   :maxdepth: 4
   :caption: Analyses

   analyses

.. toctree::
   :maxdepth: 4
   :caption: Algorithms

   algorithms

.. toctree::
   :maxdepth: 4
   :caption: Utilities

   utilities

.. toctree::
   :maxdepth: 4
   :caption: Notebooks

   notebooks

.. toctree::
   :maxdepth: 4
   :caption: Constants

   constants


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


How to contribute
=================

Contributions are welcomed and should apply the usual git-flow: fork this
repo, create a local branch named 'feature-...'. Commit often to ensure
that each commit is easy to understand. Name your commits '[feature-...]
Commit message.', such that it possible to differentiate the commits of
different features in the main line. Request a merge to the mainline often.
Please remember to follow the PEP 8 style guide, and add comments whenever
it helps. The docstring follow the Google Style Python Docstring format.
The corresponding authors are happy to support you.
