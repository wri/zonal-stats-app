import os
import simpledbf
import pandas as pd
import arcpy
import raster

from utilities import post_processing
from utilities import prep_shapefile


class Layer(object):
    """ A layer class to prep the input shapefile to zonal stats
    :param source_aoi: the path to the shapefile to run zonal stats
    :param source_id_col: the unique ID field in the input shapefile
    :return:
    """

    def __init__(self, source_aoi, source_id_col, intersect_aoi=None, intersect_aoi_col=None):

        self.source_aoi = source_aoi
        self.source_id_col = source_id_col
        self.intersect_aoi = intersect_aoi
        self.intersect_aoi_col = intersect_aoi_col

        self.final_aoi = None

        self.emissions = None
        self.forest_loss = None
        self.biomass_weight = None
        self.extent = None

        self.emissions_min_of = None
        self.emissions_max_of = None

        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        print "creating Layer with aoi {} and source id column {}".format(self.source_aoi, self.source_id_col)

    # these are all the things i want to do with the input shapefile. this is called from zonal_stats.py
    def project_source_aoi(self):
        arcpy.env.overwriteOutput = True
        out_cs = arcpy.SpatialReference(4326)
        self.final_aoi = os.path.join(self.root_dir, 'shapefile', "project.shp")
        arcpy.Project_management(self.source_aoi, self.final_aoi, out_cs)

    def intersect_source_aoi(self):
        if self.intersect_aoi:
            print "intersecting '{}' with '{}'".format(os.path.basename(self.source_aoi),
                                                       os.path.basename(self.intersect_aoi))

            self.final_aoi = prep_shapefile.intersect(self.source_aoi, self.intersect_aoi, self.root_dir,
                                                      self.intersect_aoi_col)

        else:
            print "no intersect aoi"
            self.final_aoi = self.source_aoi

    def join_tables(self, threshold, user_def_column_name, intersect=None, intersect_col=None):
        print "joining tables"

        # make a list of all the tables we have. These are already dataframes
        possible_dfs = [self.emissions, self.forest_loss, self.biomass_weight, self.forest_extent]
        df_list = [x for x in possible_dfs if x is not None]

        # how to get column names to keep? like extent, emissions, loss? i'm going through and getting
        # third column for each df which is the analysis name
        analysis_names = [x.columns.values[3] for x in df_list]

        # join all the data frames together on Value and ID
        merged = pd.concat([df.set_index(['VALUE', 'ID']) for df in df_list], axis=1)
        merged = merged.reset_index()

        # To 2 get outputs from a single function and apply to 2 different columns in the dataframe:
        # http://stackoverflow.com/questions/12356501/pandas-create-two-new-columns-in-a-dataframe-with-
        # values-calculated-from-a-pre?rq=1
        # tcd and year columns is equal to the first and second output from the function: value_to_tcd_year
        merged['tcd'], merged['year'] = zip(*merged["VALUE"].map(post_processing.value_to_tcd_year))

        # the value_to_tcd_year function is good for when user runs all thresholds, but not just one.
        # so, overwrite the tcd column when it comes back
        if threshold != "all":
            merged['tcd'] = "> {}%".format(threshold)

        # get the input table into df format
        final_aoi_dbf = self.final_aoi.replace(".shp", ".dbf")
        final_aoi_dbf = simpledbf.Dbf5(final_aoi_dbf)

        # convert dbf to pandas dataframe
        final_aoi_df = final_aoi_dbf.to_dataframe()

        # drop columns not needed

        columns_to_keep = ['ID', 'tcd', 'year']
        columns_to_keep.extend(analysis_names)

        if user_def_column_name:

            columns_to_keep.append(user_def_column_name)

        if intersect:

            columns_to_add = post_processing.generate_list_columns(intersect, intersect_col)
            columns_to_keep.extend(columns_to_add)


        final_aoi_df = final_aoi_df.drop([x for x in list(final_aoi_df.columns.values) if x not in columns_to_keep], 1)

        final_aoi_df = final_aoi_df.reset_index()

        merged_reset = merged.reset_index()

        # join the input shapefile to the output table results
        joined = merged_reset.merge(final_aoi_df, how='left', left_on="ID", right_index=True)

        joined = joined[columns_to_keep]
        # write final output to csv
        final_output_csv = os.path.join(self.root_dir, 'result', 'final_output.csv')
        joined.to_csv(final_output_csv)