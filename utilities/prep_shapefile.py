import os

import arcpy


def intersect_file(intersect_file, intersect_col=None):

    intersect_aoi_basename = os.path.basename(intersect_file)
    intersect_calc = {'adm2': """!FC_NAME! +"_"+!ISO!+ str(!ID_1!)+'d'+ str(!ID_2!)""",
                      'adm1': """!FC_NAME! +"_"+!ISO!+ str(!ID_1!)""",
                      'adm0': """!FC_NAME! +"_"+!ISO!"""}

    try:

        return intersect_calc[intersect_aoi_basename]

    except:

        print "user defined intersect field"
        exp = """!FC_NAME!+"_"+str(!{}!)""".format(str(intersect_col))

        return exp


def intersect(final_aoi, intersect_aoi, root_dir, intersect_col=None):

    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = os.path.join(root_dir, 'shapefile')

    intersected_file = os.path.join(root_dir, 'shapefile', "intersect.shp")
    arcpy.Intersect_analysis([final_aoi, intersect_aoi], intersected_file)

    print "intersected with boundary\n"

    return intersected_file


def zonal_stats_mask(final_aoi, i):

    workspace = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shapefile")

    exp = """"FID" = {}""".format(int(i))

    mask = os.path.join(workspace, "shapefile.shp")

    arcpy.FeatureClassToFeatureClass_conversion(final_aoi, workspace, "shapefile.shp", exp)

    return mask


def delete_database():
    tables_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    zstats_results_db = os.path.join(tables_dir, 'tables', 'zstats_results_db.db')
    if os.path.exists(zstats_results_db):
        print "deleting database"
        os.remove(zstats_results_db)


def build_analysis(analysis_requested):
    if 'emissions' in analysis_requested:
        analysis_requested += ['emissions_min_of', 'emissions_max_of']
        analysis_requested.remove('emissions')
        if not "forest_loss" in analysis_requested:
            analysis_requested.append('forest_loss')

    return analysis_requested
