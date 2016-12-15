import os
from data_types.layer import Layer
from data_types.raster import Raster
from raster_functions import raster_prep
from utilities import zstats_handler, post_processing, prep_shapefile


def zonal_stats(shapefile, analysis_requested, threshold, geodatabase, user_def_column_name=None, intersect=None,
                intersect_col=None):

    col_name = "FID"  # if this is in a gdb, make sure it assigns it OBJECT_ID

    # delete existing database so duplicate data isn't appended
    prep_shapefile.delete_database()

    # if user requests emissions analysis, need to runs 2 zonal stats, one min, one max.
    analysis_requested = prep_shapefile.build_analysis(analysis_requested)

    # remap the tcd mosaic and apply a raster function that adds tcd + loss year mosaics
    raster_prep.remap_threshold(geodatabase, threshold)

    l = Layer(shapefile, col_name, intersect, intersect_col)
    l.final_aoi = shapefile
    l.intersect_source_aoi()

    for analysis_name in analysis_requested:

        r = Raster(analysis_name, geodatabase)
        # run zstats, put results into sql db
        zstats_handler.main_script(l, r)
        # get results from sql to pandas df
        r.merge_results(l)

        # set attribute emissions_max_of on the layer object to be equal to emissions max of df
        print 'setting attribute {} on object {} to be equal to the df for {}'.format(analysis_name, l, analysis_name)
        setattr(l, analysis_name, r.df)

    if l.emissions_min_of is not None:
        print "processing emissions"
        l.emissions = post_processing.process_emissions(l)

    l.join_tables(threshold, user_def_column_name, intersect, intersect_col)

# types of analysis: ['emissions', 'forest_loss', 'forest_extent', 'biomass_weight']
analysis_requested = ["forest_loss", 'emissions']

shape_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shapefile')
shapefile = os.path.join(shape_dir, "test_boundary.shp")
# threshold options: 10, 15, 20, 25, 30, 50, 75, "all"
threshold = "all"
geodatabase = r"C:\Users\samantha.gibbes\Documents\gis\sample_tiles\mosaics.gdb"
user_def_column_name = "FC_NAME"

intersect = r"C:\Users\samantha.gibbes\Documents\gis\admin_boundaries\gadm27_levels.gdb\adm2"
# intersect_col = "FID"

zonal_stats(shapefile, analysis_requested, threshold, geodatabase, user_def_column_name)
