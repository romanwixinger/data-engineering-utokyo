# Data Engineer UTokyo

A software package developed for the Center of Nuclear Studies (CNS) to join all data sources and analyze the data in real-time. The package saves a lot of time by providing an easy-to-use interface for interacting with the data and allows to automatically extract key results from the data via Maximum Likelihood Estimation (MLE) and search algorithms. 

## Sources

The package can map csv files created by LabView to pandas dataframes in real-time up to a sampling rate. Examples include data from the SSD, PMT, Coil, Heater, Gauge, Laser, Ion and CCD camera. One can process new formats easily, be creating a child class of Recorder and just overriding the behaviour which has to differ from the default. 

## Outputs
The output comes in two forms of recorders and analyses. The recorders abstract away loading the csv file as pandas dataframe and keeping it up to date when more data comes in. It also provides a solution for handling csv file which are to large for pandas by introducing a parser mode. Each time we evaluate the parser, it provides us with the next chunk of data as pandas dataframe. 

## Impressions
The plot and histogram are visualizations of the SSD data. The peaks and the background are fitted with an algorithm. <br> 

<img src="impressions\SSD_Peak_Overview_Plot.png" alt="SSD Overview"  height="210"/>
<img src="impressions\SSD_Peak_Histogram.png" alt="SSD Histogram" width="300" height="210"/>
<br>

This 2D plot is obtained by Maximum Likelihood Estimation with a Gaussian model on an image from the CCD camera. <br>
<img src="impressions\CCD_2D_Gaussian.png" alt="2D Gaussian fit from CCD camera image" width="288"/>


## Example 
How to use the package to track your own csv files. 

```python
from recorders.ssd_recorder import SSDRecorder

ssd_recorder = SSDRecorder(filepath="my_filepath.csv")
df = ssd_recorder.get_table() #  Data joined with metadata
metadata_df = ssd_recorder.get_metadata()  # Just metadata
````

Next we can setup analyses which perform MLE and visualize the data. 

```python
from analyses.ssd_analyses import SSDAnalysis

ssd_analysis = SSDAnalysis(
  filepath="../../data/20220829/-20220829-144945-Slot1-In1.csv", 
  image_src="../../plots/",
  image_extension=".png"
)
ssd_analysis.run()
````

Last, we can also use a runner to perform many analyses in real-time during an experiment. 

```python

from analyses.runner import Runner
from analyses.ssd_analyses import SSDAnalysis
from analyses.pmt_analyses import PMTAnalysis

runner = Runner(analyses=[
  SSDAnalysis(filepath="../../data/20220829/-20220829-144945-Slot1-In1.csv",
              image_src="../../plots/mock"),
  PMTAnalysis(filepath="../../data/sample/all_data.csv",
              image_src="../../plots/mock")
])

# Run analyses each minute for three hours 
runner.run(cycles=3*60, period_s=60)
````

**Note:** TODO.


## Issues 

TODO

## Pull Requests

If you have something to add or new idea to implement, you are welcome to create a pull requests on improvement.

## Give it a Star

If you find this repo useful , give it a star so as many people can get to know it.

## Credits

All the credits to Roman Wixinger, supervised by Naoya Ozawa. 
