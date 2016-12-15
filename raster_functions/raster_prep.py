import os
import arcpy


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
