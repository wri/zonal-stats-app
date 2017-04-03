# zonal_stats_app

Prepping Data:
You will need to build at least 3 mosaics in ArcGIS. 
1) Loss Data. Name: loss
2) Tree Cover Density. Name: tcd
3) Area. Name: area

The only parameters that are mandatory are name and coordinate system. They must all be in WGS84 projection.

If analyzing biomass density or emissions, create a fourth mosaic:
4) Emissions Tiles (for users of procanalysis01: S:\biomass\mtc02). Name: biomass

You will also need to apply one function to the loss mosaic. This adds loss year to tcd bin.

To do this, in the catalog view, right click the loss mosaic -> properties. Under the "functions" tab, right click "Mosaic Function" -> Insert Function -> Arithmetic. Under the "Arithmetic tab", for "Input Raster 2", navigate and select the "tcd" mosaic you just createad. Input Raster 2 should now say "tcd". Click OK.
