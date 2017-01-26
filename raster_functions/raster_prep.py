import os
import arcpy
import csv
from utilities import prep_shapefile


def remap_threshold(geodatabase, threshold):
    print "remaping mosaics in {} to {}".format(geodatabase, threshold)
    this_dir = os.path.dirname(os.path.abspath(__file__))
    remap_func = os.path.join(this_dir, "remap_gt" + str(threshold) + ".rft.xml")
    loss_tcd_function = os.path.join(os.path.join(this_dir, "loss_tcd.rft.xml"))

    dict = {"tcd": remap_func, "loss": loss_tcd_function}

    for key in dict:
        mosaic_location = os.path.join(geodatabase, key)
        function = dict[key]

        arcpy.EditRasterFunction_management(mosaic_location, "EDIT_MOSAIC_DATASET", "REMOVE", function)
        arcpy.EditRasterFunction_management(mosaic_location, "EDIT_MOSAIC_DATASET", "INSERT", function)


def output_ras_table(input_raster, avg_pix_size):

    this_dir = os.path.dirname(os.path.abspath(__file__))

    # build raster attribute table
    print "build raster table"
    arcpy.BuildRasterAttributeTable_management(input_raster, "Overwrite")

    # write attribute table to text file, while calculating area
    raster_text = os.path.join(this_dir, "raster_table.csv")
    print input_raster
    with open(raster_text, "wb") as csv_file:
        csv_writer = csv.writer(csv_file)
        with arcpy.da.SearchCursor(input_raster, ["Value", "Count"]) as rows:
            row_counter = 0
            for row in rows:
                row_counter += 1
                val = row[0]
                count = row[1]
                area = count * avg_pix_size
                csv_writer.writerow([val, count, area])

    return raster_text, row_counter

# output_ras_table(r'C:\Users\samantha.gibbes\Documents\gis\test\small_raster.tif', 724.07)