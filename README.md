# Data Engineering UTokyo

A software package developed for the Center of Nuclear Studies (CNS) to join all data sources and analyze the data in real-time. The package saves a lot of time by providing an easy-to-use interface for interacting with the data and allows to automatically extract key results from the data via Maximum Likelihood Estimation (MLE) and search algorithms. 

## Data sources

The package can map csv files created by LabView to pandas dataframes in real-time up to a sampling rate in linear time, providing a quadratic speedup compared to reloading the data. Examples include data from the SSD, PMT, Coil, Heater, Gauge, Laser, Ion and CCD camera. One can process new formats easily, be creating a child class of Recorder and just overriding the behaviour which has to differ from the default. 

## Outputs
The output comes in the of recorders and analyses. The recorders abstract away loading the csv file as pandas dataframe and keeping it up to date when more data comes in. The analyses take the recorders, visualize their data, calculate or fit some metrics and store the result as csv file. 

The recorders also come in a flavor that we call parser. Parsers provide a solution for handling csv file which are to large for pandas. Each time we evaluate a parser, it provides us with the next chunk of data as pandas dataframe, without loading the full dataframe at any point in time.

## Impressions
The plot and histogram are visualizations of the SSD data. The peaks and the background are fitted with an algorithm. <br> 

<img src="impressions\SSD_Peak_Overview_Plot.png" alt="SSD Overview"  height="210"/>
<img src="impressions\SSD_Peak_Histogram.png" alt="SSD Histogram" width="300" height="210"/>
<br>

This 2D plot is obtained by Maximum Likelihood Estimation with a Gaussian model on an image from the CCD camera. <br>
<img src="impressions\CCD_2D_Gaussian.png" alt="2D Gaussian fit from CCD camera image" width="288"/>

## How to get started
There are two environments in which this package has been tested: 

### Locally 
You can clone the repository to your local computer, load the data to your computer, and run the code either in a Jupyter notebook or in a Python file. Checkout src/main.py as reference. 

Make sure that in the beginning of your code you adjust the environment such that the src folder is known. If you create your code in the analyses folder, then you have to go up two levels to reach the source folder, so you use the following code. 

```python
import sys
sys.path.insert(0,'../..')  
```

### Google Colaboratory
You create a Google Account, ask for access to the Google Drive folder, create your own alias of the folder such that you see it in your on files, start Google Colaboratory and create a new notebook. In this notebook, you have to make sure that you import your Google Drive folder. In a first step, you just mount Google Drive. 

```python
from google.colab import drive
drive.mount('/content/drive')

filepath_drive = "/content/drive/.shortcut-targets-by-id/something/some_folder"
```

Then, you navigate to the Google Drive folder with commands like
```python
cd /content/drive/
```
and 
```python
ls
```
The latter will output the files and folders which are located at your current position. When you have found the place of your folder, you save it as code like this:

```python
filepath_drive = "/content/drive/.shortcut-targets-by-id/something/some_folder"
```

Next, you navigate to your drive and clone this repository with the instructions provided on Github. You can use this [Medium article](https://medium.com/@ashwindesilva/how-to-use-google-colaboratory-to-clone-a-github-repository-e07cf8d3d22b) as reference. Navigate to the repository and verify that you are on the right branch with
```python
!git status
```

Now you can start to import functionality from the package as described in the examples. 

## Examples
How to use the package to track your own csv files. 

```python
from src.recorders.ssd_recorder import SSDRecorder

ssd_recorder = SSDRecorder(filepath="my_filepath.csv")
df = ssd_recorder.get_table()               # Full table
metadata_df = ssd_recorder.get_metadata()   # Just metadata
```

Next we can setup analyses which performs MLE and visualize the data. 

```python
from src.analyses.ssd_analyses import SSDAnalysis

ssd_analysis = SSDAnalysis(
  recorder=ssd_recorder, 
  image_src="../../plots/",
  image_extension=".png"
)
ssd_analysis.run()
```

Last, we can also use a runner to perform many analyses in real-time during an experiment. 

```python
from src.analyses.runner import Runner
from src.analyses.ssd_analyses import SSDAnalysis
from src.analyses.pmt_analyses import PMTAnalysis

analyses = [
  SSDAnalysis(recorder=ssd_recorder, image_src="../../plots/mock"),
  PMTAnalysis(recorder=pmt_recorder, image_src="../../plots/mock")
]
runner = Runner(analyses=analyses)
runner.run(cycles=3*60, period_s=60) # Every 60 seconds for three hours 
````

Sometimes, we want to perform the same analysis on many different files. Then, we can leverage the FileRecorder to find the filenames, paths and creation times of these files. 

```python
from src.recorders.file_recorder import FileRecorder

file_recorder = FileRecorder(
  filepath="path_to_the_folder/", 
  match="regex_pattern_to_find_the_right_files"
)
file_df = file_recorder.get_table()
````

From time to time, we want to test our analysis with a recorder that represents data that we know well. For this purpose, we introduce the StaticRecorder. This class behaves like a recorder, but its data is a fixed dataframe given upon initialization.

```python
import pandas as pd

from src.recorders.static_recorder import StaticRecorder

df = pd.DataFrame(
  data=[["Alice", 25], ["Bob", 23], ["Eve", 27]], 
  columns=["name", "age"]
  )
static_recorder = StaticRecorder(df=df)
````


## Issues 

There are a few issues which need further consideration. 

## Pull Requests

If you have something to add or new idea to implement, you are welcome to create a pull requests on improvement.

## Give it a Star

If you find this repo useful , give it a star so as many people can get to know it.

## Credits

All the credits go to Roman Wixinger and Shintaro Nagase, supervised by Naoya Ozawa and with help from Teruhito Nakashita and Keisuke Nakamura. 
