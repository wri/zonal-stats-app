import os
import datetime

start = datetime.datetime.now()
from data_types.layer import Layer
from data_types.raster import Raster
from raster_functions import raster_prep
from utilities import zstats_handler, post_processing, prep_shapefile, config_parser


# get user inputs from config file:
config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config_file.ini")
config_dict = config_parser.read_config(config_file)

# analysis: forest_extent, forest_loss, biomass_weight, emissions
analysis = [x.strip() for x in config_dict['analysis'].split(",")]
shapefile = config_dict['shapefile']
threshold = config_dict['threshold']
geodatabase = config_dict['geodatabase']
intersect = config_dict['intersect']
intersect_col = config_dict['intersect_col']
user_def_column_name = config_dict['user_def_column_name']
col_name = "FID"  # if this is in a gdb, make sure it assigns it OBJECT_ID
method = config_dict['method']  # zonal_stats or average_area
output_file_name = config_dict['output_file_name']

# delete existing database so duplicate data isn't appended
prep_shapefile.delete_database()

# if user requests emissions analysis, need to runs 2 zonal stats, one min, one max.
analysis_requested = prep_shapefile.build_analysis(analysis)

# remap the tcd mosaic and apply a raster function that adds tcd + loss year mosaics
raster_prep.remap_threshold(geodatabase, threshold)

# create layer object. this just sets up the properties that will later be filled in for each analysis
l = Layer(shapefile, col_name, intersect, intersect_col)

# set final aoi equal to the shapefile
l.final_aoi = shapefile

# project input to wgs84
l.project_source_aoi()

# if we set an intersection layer, this will evaluate. otherwise, final aoi = source aoi
l.intersect_source_aoi()

for analysis_name in analysis_requested:
    # create raster object.
    r = Raster(analysis_name, geodatabase)

    # run zstats, put results into sql db. for emissions, will have emissions_max_of, min_of
    zstats_handler.main_script(l, r, method)

    # get results from sql to pandas df
    r.merge_results(l)

    # set attribute emissions_max_of on the layer object to be equal to emissions max of df
    # if not doing min/max, do i need to do this??
    print 'setting attribute {} on object {} to be equal to the df for {}'.format(analysis_name, l, analysis_name)
    setattr(l, analysis_name, r.df)

if l.emissions is not None:
    print "processing emissions"
    l.emissions = post_processing.process_emissions(l)

# join possible tables (loss, emissions, extent, etc) and decode to loss year, tcd
l.join_tables(threshold, user_def_column_name, output_file_name, intersect, intersect_col)

print "elapsed time: {}".format(datetime.datetime.now() - start)