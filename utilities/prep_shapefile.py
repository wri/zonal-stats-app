import os
import numpy as np
import math
import arcpy


def intersect_file(intersect_file, intersect_col=None):

    intersect_aoi_basename = os.path.basename(intersect_file)
    intersect_calc = {'adm2': """!FC_NAME! +"_"+!ISO!+ str(!ID_1!)+'d'+ str(!ID_2!)""",
                      'adm1': """!FC_NAME! +"_"+!ISO!+ str(!ID_1!)""",
                      'adm0': """!FC_NAME! +"_"+!ISO!"""}

    try:

        return intersect_calc[intersect_aoi_basename]

    except:

        print("user defined intersect field")
        exp = """!FC_NAME!+"_"+str(!{}!)""".format(str(intersect_col))

        return exp


def intersect(final_aoi, intersect_aoi, root_dir, intersect_col=None):

    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = os.path.join(root_dir, 'shapefile')

    intersected_file = os.path.join(root_dir, 'shapefile', "intersect.shp")
    arcpy.Intersect_analysis([final_aoi, intersect_aoi], intersected_file)

    print("intersected with boundary\n")

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
        print("deleting database")
        os.remove(zstats_results_db)


def build_analysis(analysis_requested):
    # if analysis is emissions, we still need to run forest_loss
    if not "forest_loss" in analysis_requested:
        analysis_requested.append('forest_loss')

    return analysis_requested


def get_area(geom):
    """
    Calculate geodesic area for Hansen data, assuming a fix pixel size of 0.00025 * 0.00025 degree
    using WGS 1984 as spatial reference.
    Pixel size various with latitude, which is it the only input parameter.
    """

    lat = geom.projectAs("WGS 1984").centroid.Y

    a = 6378137.0  # Semi major axis of WGS 1984 ellipsoid
    b = 6356752.314245179  # Semi minor axis of WGS 1984 ellipsoid

    d_lat = 0.00025  # pixel hight
    d_lon = 0.00025  # pixel width

    pi = math.pi

    q = d_lon / 360
    e = math.sqrt(1 - (b / a) ** 2)

    area = abs((pi * b ** 2 * (
    2 * np.arctanh(e * np.sin(np.radians(lat + d_lat))) / (2 * e) + np.sin(np.radians(lat + d_lat)) / (
    (1 + e * np.sin(np.radians(lat + d_lat))) * (1 - e * np.sin(np.radians(lat + d_lat)))))) - (pi * b ** 2 * (
    2 * np.arctanh(e * np.sin(np.radians(lat))) / (2 * e) + np.sin(np.radians(lat)) / (
    (1 + e * np.sin(np.radians(lat))) * (1 - e * np.sin(np.radians(lat))))))) * q

    return area


def average_pixel_size(mask):

    with arcpy.da.SearchCursor(mask, 'SHAPE@') as cursor:
        for row in cursor:

            avg_pix_size = get_area(row[0])

            print(avg_pix_size)
    return avg_pix_size
