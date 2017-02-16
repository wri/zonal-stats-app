import os
import arcpy
import csv


def remap_threshold(geodatabase, threshold):
    # the loss mosaic should have a function applied to it 1 time and never gets touched after.
    # the only function to be swapped out is for remap
    print "remaping mosaics in {} to {}".format(geodatabase, threshold)
    this_dir = os.path.dirname(os.path.abspath(__file__))
    remap_func = os.path.join(this_dir, "remap_gt" + str(threshold) + ".rft.xml")

    mosaic_location = os.path.join(geodatabase, "tcd")

    arcpy.EditRasterFunction_management(mosaic_location, "EDIT_MOSAIC_DATASET", "REMOVE", remap_func)
    arcpy.EditRasterFunction_management(mosaic_location, "EDIT_MOSAIC_DATASET", "INSERT", remap_func)


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