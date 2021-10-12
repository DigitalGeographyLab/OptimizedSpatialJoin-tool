'''
This script serves for connection of OptiSS tool with ArcPy 3.6 from
ArcGIS Pro 2.2. This enrichment process help to the creation of a enriched social media
posting history dataset that can be used for further processes such as
Origin (home) Detection (country, county, municipality)

Author: Bryan R. Vallejo/Digital Geography Lab
Project: Borderspace Project
Date: 09-2021
'''
import arcpy
import os

# directory
homefolder = os.getcwd()
# homefolder = os.path.dirname(os.getcwd())

workspace = os.path.join(homefolder, 'arcpy_env.gdb')

# URL defined by sys
try:
    regions_name = str(sys.argv[1])
except:
    pass

# Check if there is Environemnt GDB
if os.path.isdir(workspace):
    pass
else:
    gdb_file = arcpy.management.CreateFileGDB(homefolder, 'arcpy_env.gdb')

# Enable output overwriting.
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

# _____________________________1. Copy to Workspace_____________________________
# shp of social media posting history
input_geodata = os.path.join(homefolder, r'app_data\geodata\some_geodata.shp')
some_geodata = os.path.join(workspace, r'some_geodata')

# copy to workspace
if os.path.isdir(some_geodata):
    pass
else:
    arcpy.conversion.FeatureClassToGeodatabase(input_geodata, workspace)
    # arcpy.management.RepairGeometry(some_geodata, 'DELETE_NULL', 'ESRI')

# _____________________________2. Spatial join_____________________________



regions_path = os.path.join(homefolder, 'regions_layer\{}'.format(regions_name))

regions_layername = os.path.basename(regions_path)[:-4]

regions_gdbname = os.path.join(workspace, regions_layername)

# copy to workspace
if os.path.isdir(regions_layername):
    pass
else:
    arcpy.conversion.FeatureClassToGeodatabase(regions_path, workspace)

arcpy.management.AddSpatialIndex(regions_gdbname, 0, 0, 0)
arcpy.management.AddSpatialIndex(some_geodata, 0, 0, 0)

# INLAND and OUTLAND
print('Working in Inland posts')
inland_posts = arcpy.management.SelectLayerByLocation(some_geodata,
                                                    "WITHIN", regions_gdbname,
                                                    None,"NEW_SELECTION",
                                                    "NOT_INVERT")
print('Working in Outland posts')
outland_posts = arcpy.management.SelectLayerByLocation(some_geodata,
                                                    "WITHIN", regions_gdbname,
                                                    None, "NEW_SELECTION",
                                                    "INVERT")

# SPATIAL JOIN
outFile = os.path.join(workspace, os.path.basename(some_geodata)+'_joined')

print('Working in Inland join')
inland_join = arcpy.analysis.SpatialJoin(inland_posts, regions_gdbname, outFile + '_inland',
                                         "JOIN_ONE_TO_ONE", "KEEP_ALL", '#',
                                         "WITHIN",
                                         None,
                                         "distance")

print('Working in Outland join')
outland_join = arcpy.analysis.SpatialJoin(outland_posts, regions_gdbname, outFile + '_outland',
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
if os.path.isdir(optiss_data_gdb):
    arcpy.management.CopyFeatures(optiss_data_gdb, optiss_demo_data,'', None, None, None)
else:
    arcpy.management.Merge(mergefiles, optiss_data_gdb, '#', "NO_SOURCE_INFO")
    arcpy.management.CopyFeatures(optiss_data_gdb, optiss_demo_data,'', None, None, None)
print('Optimization done')
