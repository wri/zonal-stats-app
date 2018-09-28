import os
import arcpy
import csv


def remap_threshold(geodatabase, threshold):

    # Apply a remap function to the tcd mosaic. Turns values of TCD into bins recoded to
    # values of 40, 80, etc.
    print("remaping mosaics in {} to {}".format(geodatabase, threshold))
    this_dir = os.path.dirname(os.path.abspath(__file__))
    remap_func = os.path.join(this_dir, "remap_gt" + str(threshold) + ".rft.xml")
    tcd_mosaic = os.path.join(geodatabase, "tcd")

    arcpy.EditRasterFunction_management(tcd_mosaic, "EDIT_MOSAIC_DATASET", "REPLACE", remap_func)


def output_ras_table(input_raster, avg_pix_size):

    this_dir = os.path.dirname(os.path.abspath(__file__))

    # build raster attribute table
    print("build raster table")
    arcpy.BuildRasterAttributeTable_management(input_raster, "Overwrite")

    # write attribute table to text file, while calculating area
    raster_text = os.path.join(this_dir, "raster_table.csv")

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
