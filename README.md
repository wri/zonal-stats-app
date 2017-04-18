# zonal_stats_app
### Overview
This tool is intended for the specific task of calculating area of loss within the UMD Hansen forest loss product. 


### Data Prep
You will need to build at least 3 mosaics in ArcGIS. Name them exactly as below. The only parameters that are mandatory are name and coordinate system. They must all be in WGS84 projection.

Mosaic Name | Data within Mosaic
----- | -----
loss | Hansen Loss tiles
tcd | Hansen Tree Cover Extent tiles
area | Custom Built Area Tiles



If analyzing biomass density or emissions, create a fourth mosaic:
4) Emissions Tiles (for users of procanalysis01: S:\biomass\mtc02). Name: biomass

You will also need to apply one function to the loss mosaic. This adds loss year to tcd bin.

To do this, in the catalog view, right click the loss mosaic -> properties. Under the "functions" tab, right click "Mosaic Function" -> Insert Function -> Arithmetic. Under the "Arithmetic tab", for "Input Raster 2", navigate and select the "tcd" mosaic you just createad. Input Raster 2 should now say "tcd". Click OK.
