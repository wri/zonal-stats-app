import sys
import os
import arcpy
import pandas
import sqlite3

import prep_shapefile
from raster_functions import raster_prep

arcpy.CheckOutExtension("Spatial")

value = sys.argv[1]
zone = sys.argv[2]
final_aoi = sys.argv[3]
cellsize = sys.argv[4]
analysis = sys.argv[5]
start = int(sys.argv[6])
stop = int(sys.argv[7])

arcpy.env.overwriteOutput = True

for i in range(start, stop):
    print i

    # to adapt for new zonal stats (which isn't zonal stats), extract by mask, create raster
    # get raster attribute table to make list of 1 column: pixel value 1 column: count
    # then, calculate average pixel size on polygon
    # multiple count by pixel size.
    tables_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tables')

    # select one individual feature from the input shapefile
    print "prepping shapefile"
    mask = prep_shapefile.zonal_stats_mask(final_aoi, i)

    # calculate average pixel size based on just the shapefile and an area formula
    print "calculating average pixel size"
    avg_pix_size = prep_shapefile.average_pixel_size(mask)

    # extract loss/tcd within the shapefile
    print "extract by mask"
    outputdir = os.path.dirname(mask)
    output_tif = os.path.join(outputdir, "extract_loss.tif")

    arcpy.gp.ExtractByMask_sa(zone, mask, output_tif)

    # # create table of loss/tcd codes with count
    raster_text, row_counter = raster_prep.output_ras_table(output_tif, avg_pix_size)

    # # convert csv to dataframe
    df = pandas.DataFrame.from_csv(raster_text)
    df = df.reset_index()
    df.columns = ['VALUE', 'COUNT', 'SUM']

    df['ID'] = i
    df[analysis] = df['SUM']

    # name of the sql database to store the sql table
    zstats_results_db = os.path.join(tables_dir, 'zstats_results_db.db')

    # create a connection to the sql database
    conn = sqlite3.connect(zstats_results_db)

    # append the dataframe to the database
    df.to_sql(analysis, conn, if_exists='append')

    # delete these because they create a lock
    del df

    # reset these environments. Otherwise the shapefile is redefined based on features within the extent
    arcpy.env.extent = None
    arcpy.env.mask = None
    arcpy.env.cellSize = None
    arcpy.env.snapRaster = None

    print 'process succeeded for id {0}'.format(i)
