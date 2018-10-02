import os
import datetime

import logging
# configure log file
logging.basicConfig(filename='log_zonal_stats.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.getLogger().addHandler(logging.StreamHandler())

from data_types.layer import Layer
from data_types.raster import Raster
from raster_functions import raster_prep
from utilities import zstats_handler, post_processing, prep_shapefile, config_parser

start = datetime.datetime.now()
logging.debug("\n\nHello! This is the beginning of the log")

# get user inputs from config file:
config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config_file.ini")
config_dict = config_parser.read_config(config_file)

# analysis: forest_extent, forest_loss, biomass_weight, emissions
analysis = [x.strip() for x in config_dict['analysis'].split(",")]
shapefile = config_dict['shapefile']
threshold = config_dict['threshold']
geodatabase = config_dict['geodatabase']
user_def_column_name = config_dict['user_def_column_name']
col_name = "FID"  # if this is in a gdb, make sure it assigns it OBJECT_ID
output_file_name = config_dict['output_file_name']

# delete existing database so duplicate data isn't appended
prep_shapefile.delete_database()

# if user requests emissions analysis, need to runs 2 zonal stats, one min, one max.
analysis_requested = prep_shapefile.build_analysis(analysis)

# remap the tcd mosaic and apply a raster function that adds tcd + loss year mosaics
raster_prep.remap_threshold(geodatabase, threshold)

# create layer object. this just sets up the properties that will later be filled in for each analysis
l = Layer(shapefile, col_name)

# set final aoi equal to the shapefile
l.final_aoi = shapefile

# project input to wgs84
l.project_source_aoi()

# loop over the analysis. If forest_loss or biomass_weight, will just be one analysis. if emissions, need to
# run forest_loss and emissions

for analysis_name in analysis_requested:
    # create raster object.
    r = Raster(analysis_name, geodatabase)

    # run zstats, put results into sql db. 
    zstats_handler.main_script(l, r)

    # get results from sql to pandas df
    r.db_to_df(l)

    # this roughly translate to layer.analysis_name == r.df
    # or forest_loss = pd.DataFrame(forestlossdata). It gives the resulting dataframe the name of the analysis and sets
    # it as the attribute l.forest_loss, l.emissions, which are the dataframes
    setattr(l, analysis_name, r.df)

if l.emissions is not None:
    print("converting biomass to emissions")
    l.emissions = post_processing.biomass_to_mtc02(l)

# join possible tables (loss, emissions, extent, etc) and decode to loss year, tcd
l.join_tables(threshold, user_def_column_name, output_file_name)

logging.debug(("elapsed time: {}".format(datetime.datetime.now() - start)))