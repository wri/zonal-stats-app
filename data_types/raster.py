import os
import pandas as pd
import sqlite3


class Raster(object):
    """ A layer class to prep the input shapefile to zonal stats
    :param source_aoi: the path to the shapefile to run zonal stats
    :param source_id_col: the unique ID field in the input shapefile
    :return:
    """

    def __init__(self, analysis, geodatabase):
        print "\ncreating a raster object for analysis {}".format(analysis)
        self.analysis = analysis
        self.zone = None
        self.value = None
        self.geodatabase = geodatabase
        self.cellsize = None
        self.output_tables = []
        self.df = None

        self.populate_ras_prop()

    def populate_ras_prop(self):
        zone_value_dict = {"forest_loss": {"zone": "loss", "value": "area", "cellsize": "MAXOF"},
                           "emissions_max_of": {"zone": "loss", "value": "biomass", "cellsize": "MAXOF"},
                           "emissions_min_of": {"zone": "loss", "value": "biomass", "cellsize": "MINOF"},
                           "forest_extent": {"zone": "tcd", "value": "area", "cellsize": "MAXOF"},
                           "biomass_weight": {"zone": "tcd", "value": "biomass", "cellsize": "MAXOF"},
                           "emissions": {"zone": "loss", "value": "biomass", "cellsize": "MAXOF"}}

        self.zone = os.path.join(self.geodatabase, zone_value_dict[self.analysis]["zone"])
        self.value = os.path.join(self.geodatabase, zone_value_dict[self.analysis]["value"])
        self.cellsize = zone_value_dict[self.analysis]['cellsize']

        print "populating raster properties with zone: {} and value: {} and cell size {}".format(os.path.basename(self.zone),
                                                                                os.path.basename(self.value),
                                                                                                 self.cellsize)

    def merge_results(self, l):

        # convert sql table to df
        print "converting sql table to df"
        tables_dir = os.path.join(l.root_dir, 'tables')
        zstats_results_db = os.path.join(tables_dir, 'zstats_results_db.db')

        conn = sqlite3.connect(zstats_results_db)
        # self.analysis is like: forest_loss and/or emissions, etc
        qry = "SELECT VALUE, ID, SUM, {0} FROM {0} WHERE VALUE > 19".format(self.analysis)

        df = pd.read_sql(qry, conn)

        self.df = df
