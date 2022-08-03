# zonal-stats-app
### Overview
This tool is intended for the specific task of calculating area of loss within the University of Maryland's (UMD) Hansen forest loss product. The basic steps to create a CSV of forest loss and/or emissions are:

1. Create a File Geodatabase in ArcGIS
2. Build the 3 mosaics needed for the forest loss analysis. If analyzing emissions, also build a Biomass mosaic
3. Apply an Arithmetic function to the Loss mosaic
    1. If analyzing emissions, also apply an Arithmetic function to the Biomass mosaic 
4. Edit the config file specify the parameters of your analysis
5. Run the code
6. View the CSV of results

The code works by creating unique "bins" of data to collect area pixels which are then summed within each bin using ArcGIS Zonal Statistics. The bins are the combination of 1) loss year and 2) tree cover density. This allows the tool to summarize loss for all years and at any of the pre-defined tree cover density thresholds: 10, 15, 20, 25, 30, 50, 75.


### Prerequisites and dependencies

Download and install HDF5.
You will need to register and download the software [here](https://www.hdfgroup.org/downloads/hdf5/).

Download the build which matches your python instance (ie 32bit or 64bit)
Make sure the HDF installation directory is added to your environment PATH. The installation normally should take care of this.

Make sure you have the latest version of Numpy and Panda and install the following modules

```shell
pip install numpy --upgrade
pip install panda --upgrade
pip install SQLAlchemy
pip install simpledbf
pip install tables
```

PyTables requires several drivers which should come with HDF5. To make sure, everything is correctly configured, 
open your Python console and type in 
import tables

if no error message appears you are good to go, otherwise revise your installation and troubleshoot. 
More info [here](http://www.pytables.org/usersguide/installation.html).


### Data Prep

1. Build at least 3 mosaic datasets in ArcGIS. 
    1. Create a file geodatabase, right click to select "new" and "mosaic dataset." 
    2. Name them exactly as the table below. They must all be in WGS84 projection. 
    3. Right click on the empty mosaic dataset and click "add rasters". If the raster dataset is stored in a stand alone folder with no other data, keep the input data "workspace" select, navigate to the data and click ok. "Add raster to mosaic dataset" will run, and once complete a green footpint of the mosaic dataset will be filled out the raster data boundaries.

Mosaic Name | Data within Mosaic
----- | -----
loss | UMD Hansen Loss tiles
tcd | UMD Hansen Tree Cover Extent tiles
area | Custom Built Area Tiles
biomass (optional) | Woods Hole Research Center Biomass in Mg/Ha

2. Apply an Arithmetic Function to the Loss Mosaic
   1. In the catalog view of ArcGIS, right click the LOSS mosaic -> properties. 
   2. Under the "functions" tab, right click "Mosaic Function" -> Insert Function -> Arithmetic. 
   3. Under the "Arithmetic tab", for "Input Raster 2", navigate and select the "TCD" mosaic you just createad. Input Raster 2 should now say "tcd". The "Operation" shoud say "Plus". Click OK.
   <br />![loss mosaic functions](https://github.com/wri/zonal-stats-app/blob/master/images/loss_arithmetic.JPG?raw=true "Functions Applied to Loss Mosaic")
   
   
   <br />![loss mosaic functions](https://github.com/wri/zonal-stats-app/blob/master/images/loss_mosaic.JPG?raw=true "Functions Applied to Loss Mosaic")
3. Apply an Arithmetic Function to the Biomass Mosaic (if analyzing emissions). The biomass data is in Mg/ha. We want to know how much biomass is in each PIXEL. To do this, multiply the biomass pixel by the area pixel in hectares. 
   1. In the catalog view of ArcGIS, right click the BIOMASS mosaic -> properties. 
   2. Under the "functions" tab, right click "Mosaic Function" -> Insert Function -> Arithmetic. 
   3. Under the "Arithmetic tab", for "Input Raster 2", navigate and select the "AREA" mosaic you just createad. Input Raster 2 should now say "biomass". Change the "Operation" to "Multiply. Click OK.
   <br />![alt_text](https://github.com/wri/zonal-stats-app/blob/master/images/biomass_arithmetic_1.JPG?raw=true "first biomass function")
   4. Add a second function: Right click the "area" mosaic in the Function Chain. -> Insert Function -> Arithmetic.
   5. Under "Generate raster from constant" Select Raster: Raster 2
   6. Constant: 10000
   7. Click OK
   8. Click OK to close the Mosaic Dataset Properties dialogue box
   <br />![alt_text](https://github.com/wri/zonal-stats-app/blob/master/images/biomass_arithmetic_2.JPG?raw=true "second biomass function") 
   
   #### Final Biomass Mosaic Function Chain
   ![alt_text](https://github.com/wri/zonal-stats-app/blob/master/images/biomass_mosaic_function.JPG?raw=true "second biomass function") 
   
### Edit the config file
In the main folder is a file called config_file.ini.sample. Rename this to config_file.ini and fill in your specific parameters
<br />The required parameters are:
<br />**analysis**
<br />**shapefile**
<br />**threhsold**
<br />**geodatabase**
<br />**output_file_name**

Other options:
- **analysis**: forest_loss, emissions, forest_extent, biomass_weight
- **threshold**:  10, 15, 20, 25, 30, 50, 75, all. The "all" option creates each bin. 10-15, 15-20....75-100. You can then add the totals in various combinations
- **output_file_name**: the name of the output csv file
- **intersect**: if you choose to intersect the shapefile with another boundary, specify the other boundary here
- **intersect_col**: a column that uniquely identifies the intersect file
- **user_def_column_name**: by default, the code uses the FID of the shapefile to identify each feature. Here, you can specify which column uniquely identifies your input shapefile

### Run the Code
This can be done several ways. Either within a python code editor, or the most simple way, through a command prompt window.
1. Open a command prompt window from the zonal-stats-app folder
2. Type: `%python3% zonal_stats.py` (The script uses Python3, so this tells the comland line to use Python3 instead of the default Python2.)
3. Hit enter

### View the results
Results are stored in a .csv in the result folder with the output file name you specified in the config file. 
<br />![alt_text](https://github.com/wri/zonal-stats-app/blob/master/images/csv_walkthrough.jpg?raw=true "csv walkthrough")
