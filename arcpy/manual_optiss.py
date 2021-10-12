'''
OptiSS tool for optimizing spatial joining of big social media data
Arcpy 2.6 and Python 3

Script for manual usage of OptiSS. Optimize spatial join of social media posts with regions layer.
Be aware of configuring the parameters properly to be implemented in your workflow

Thanks to the methodological development of Vuokko Heikinheimo in SOME project and the
method performance evaluation of Olle Järv this app helps to researchers in the
enrichment process of social media posting history as first step
for Origin (home) Detection (country, county, municipality)

Author: Bryan R. Vallejo/Digital Geography Lab
Project: Borderspace Project
Date: 10-2021
'''

import arcpy
import os

# _____PARAMETERS_____

homefolder = os.path.dirname(os.getcwd())

# 1
name_some_data = 'twitter_posting_history_sample.csv'
input_some_data = os.path.join(homefolder, 'app_data/{}'.format(name_some_data))

# 2
name_regions_layer = 'global_regions_fixed_wgs84.shp'

region_folder = os.path.join(homefolder, 'regions_layer')
if not os.path.exists(region_folder):
    os.makedirs(region_folder)

input_regions_layer = os.path.join(homefolder, 'regions_layer/{}'.format(name_regions_layer))

#3
longitude_column = 'lon'
latitude_columns = 'lat'


# ____ ANALYSIS _____

# create environment
gdb_file = arcpy.management.CreateFileGDB(homefolder, 'arcpy_env.gdb')

workspace = os.path.join(homefolder, 'arcpy_env.gdb')

# Enable output overwriting.
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

# _____________________________1. Copy to Workspace_____________________________

# copy social media dataset
arcpy.conversion.TableToGeodatabase(input_some_data, workspace)
some_gdb = os.path.join(workspace, '{}'.format(name_some_data[:-4]))

# copy regions layer
arcpy.conversion.FeatureClassToGeodatabase(input_regions_layer, workspace)

regions_gdb = os.path.join(workspace, '{}'.format(name_regions_layer[:-4]))

# arcpy.management.RepairGeometry(regions_gdb, 'DELETE_NULL', 'ESRI')

# xy events
events = arcpy.management.MakeXYEventLayer(some_gdb, longitude_column, latitude_columns, "some_xyevents",\
                                           "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',\
                                           SPHEROID['WGS_1984',6378137.0,298.257223563]],\
                                           PRIMEM['Greenwich',0.0],\
                                           UNIT['Degree',0.0174532925199433]];\-400 -400 1000000000;-100000 10000;\
                                           -100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision",\
                                           None)

some_geodata = os.path.join(workspace, 'some_geodata')

arcpy.management.CopyFeatures(events, some_geodata,'', None, None, None)
# arcpy.management.RepairGeometry(some_geodata, 'DELETE_NULL', 'ESRI')

# _____________________________2. Spatial join_____________________________

arcpy.management.AddSpatialIndex(some_geodata, 0, 0, 0)
arcpy.management.AddSpatialIndex(regions_gdb, 0, 0, 0)

# INLAND and OUTLAND
print('Working in Inland posts')
inland_posts = arcpy.management.SelectLayerByLocation(some_geodata,
                                                    "WITHIN", regions_gdb,
                                                    None,"NEW_SELECTION",
                                                    "NOT_INVERT")

print('Working in Outland posts')
outland_posts = arcpy.management.SelectLayerByLocation(some_geodata,
                                                    "WITHIN", regions_gdb,
                                                    None, "NEW_SELECTION",
                                                    "INVERT")

# SPATIAL JOIN
outFile = os.path.join(workspace, os.path.basename(some_geodata)+'_joined')

print('Working in Inland join')
inland_join = arcpy.analysis.SpatialJoin(inland_posts, regions_gdb, outFile + '_inland',
                                         "JOIN_ONE_TO_ONE", "KEEP_ALL", '#',
                                         "WITHIN",
                                         None,
                                         "distance")

print('Working in Outland join')
outland_join = arcpy.analysis.SpatialJoin(outland_posts, regions_gdb, outFile + '_outland',
                                          "JOIN_ONE_TO_ONE", "KEEP_ALL", '#',
                                          "CLOSEST_GEODESIC", None, "distance")

# MERGE
mergefiles = outFile + '_inland' + ';' + outFile + '_outland'

optiss_data_gdb = os.path.join(workspace, 'optiss_demo_data')
optiss_folder = os.path.join(homefolder, 'optiss_result')
if not os.path.exists(optiss_folder):
    os.makedirs(optiss_folder)

optiss_demo_data = os.path.join(optiss_folder, 'optiss_demo_data.shp')

print('Merging')

arcpy.management.Merge(mergefiles, optiss_data_gdb, '#', "NO_SOURCE_INFO")
arcpy.management.CopyFeatures(optiss_data_gdb, optiss_demo_data,'', None, None, None)
print('Optimization done')














# END
