# zonal_stats_app

Prepping Data:
You will need to build 2 mosaics in ArcGIS. One to contain the tree cover density rasters, one to contain the loss data rasters. The only parameters that are mandatory are name and coordinate system. Name the loss mosaic "loss", name the tree cover density mosaic "tcd". Both must be in WGS84 projection.

You will also need to apply one function to the loss mosaic. To do this, in the catalog view, right click the loss mosaic -> properties. Under the "functions" tab, right click "Mosaic Function" -> Insert Function -> Arithmetic. Under the "Arithmetic tab", for "Input Raster 2", navigate and select the "tcd" mosaic you just createad. Input Raster 2 should now say "tcd". Click OK.
