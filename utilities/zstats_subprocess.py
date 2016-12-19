import sys
import os
import sqlite3
import simpledbf
import prep_shapefile
import arcpy
from arcpy.sa import *

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

    mask = prep_shapefile.zonal_stats_mask(final_aoi, i)

    arcpy.env.extent = mask
    arcpy.env.mask = mask
    arcpy.env.cellSize = cellsize
    arcpy.env.snapRaster = value

    tables_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tables')

    z_stats_tbl = os.path.join(tables_dir, 'output.dbf')

    print 'debug: starting zstats'

    outzstats = ZonalStatisticsAsTable(zone, "VALUE", value, z_stats_tbl, "DATA", "SUM")
    arcpy.AddMessage('debug: finished zstats')
    result = arcpy.GetCount_management(z_stats_tbl)
    count = int(result.getOutput(0))
    print "count of records in zstats table: {}".format(count)
    dbf = simpledbf.Dbf5(z_stats_tbl)

    # convert dbf to pandas dataframe
    df = dbf.to_dataframe()

    # populate a new field "id" with the FID and analysis with the sum
    df['ID'] = i
    df[analysis] = df['SUM']

    # name of the sql database to store the sql table
    zstats_results_db = os.path.join(tables_dir, 'zstats_results_db.db')

    # create a connection to the sql database
    conn = sqlite3.connect(zstats_results_db)

    # append the dataframe to the database
    df.to_sql(analysis, conn, if_exists='append')

    # delete these because they create a lock
    del df, dbf

    # reset these environments. Otherwise the shapefile is redefined based on features within the extent
    arcpy.env.extent = None
    arcpy.env.mask = None
    arcpy.env.cellSize = None
    arcpy.env.snapRaster = None

    print 'process succeeded for id {0}'.format(i)
