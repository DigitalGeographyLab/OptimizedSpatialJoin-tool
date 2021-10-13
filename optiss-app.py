'''
OptiSS tool for optimizing spatial joining of big social media data
Arcpy 2.6 and Python 3

Local app that optimize spatial join of social media posts with regions layer.
Check read me file of repository for more details of how it works.

Thanks to the methodological development of Vuokko Heikinheimo in SOME project and the
method performance evaluation of Olle Järv this app helps to researchers in the
enrichment process of social media posting history as first step
for Origin (home) Detection (country, county, municipality)

Author: Bryan R. Vallejo/Digital Geography Lab
Project: Borderspace Project
Date: 10-2021
'''

import streamlit as st
import pandas as pd
import glob
import os
import sys
import time
from datetime import datetime

import geopandas as gpd
from pyproj import CRS
from shapely.geometry import Point
import matplotlib.pyplot as plt

# directory
homefolder = os.getcwd()

# __________________FUNCTIONS___________________
def data_list():
    '''Function that gives back a list of [ULRS of files, names of files] in folder app_data'''

    files_list = glob.glob(os.path.join(homefolder, 'app_data/*.csv'))

    names_list = [os.path.basename(file) for file in files_list]

    return [files_list, names_list]

def read_data(selectbox_button):
    '''Function that reads CSV file selected in selectionbox'''
    path = os.path.join(homefolder, 'app_data/{}'.format(str(selectbox_button)))

    dataset = pd.read_csv(path, sep=';')

    return dataset

def read_geodata(selectbox_button):
    '''Function that reads CSV file selected in selectionbox'''
    path = os.path.join(homefolder, 'regions_layer/{}'.format(str(selectbox_button)))

    dataset = gpd.read_file(path)

    return dataset

def create_geomlist(dataframe, long_selection, lat_selection):
    '''Function that gives back a list of geometries of input data'''

    try:
        geom_list = [Point(lon, lat) for lon, lat in
                                    zip(dataframe[long_selection].to_list(),
                                        dataframe[lat_selection].to_list())]
        return geom_list
    except:
        st.warning('Select the correct columns!')

def plot_geodata(geodata_layer):
    '''Function that plot the GADM layer - extra functionality'''

    plt.style.use('seaborn')

    fig, ax = plt.subplots()
    geodata_layer.plot(ax=ax, facecolor="lightgray", edgecolor="black")

    plt.axis('off')
    return fig
# ______________________________________

st.title('Welcome to OptiSS 🧐')
st.header('Tool for optimizing spatial joining of big social media data')
st.write('Follow the next steps that help you in the optimization of the spatial join process. The app comes with a sample dataset of twitter posting history but you can add your own social media datasets and regions. Check instructions before using it.')
st.markdown('[How to use OptiSS?](https://github.com/DigitalGeographyLab/OptimizedSpatialJoin-tool)')

# 1.  ______________________READ SOCIAL MEDIA DATASET_________________________
st.header('1. Upload your social media posting history dataset')
st.write('Dataset must be in **.csv** and delimited by **semicolons**')

filepath = st.selectbox('Files in <app_data> folder:', options=data_list()[1])
data = read_data(filepath)
columns = list(data.columns)

st.write('**Timestamp** column, and **User ID** column are used only for displaying info (optional columns) ')
datacol1, datacol2, datacol3, datacol4 = st.columns(4)

time_col = datacol1.selectbox('Timestamp column', options=columns)
long_col = datacol2.selectbox('Longitude', options=columns)
lat_col = datacol3.selectbox('Latitude', options=columns)
userid_col = datacol4.selectbox('User ID', options=columns)

# DATA
data = pd.DataFrame(data[[time_col, long_col, lat_col, userid_col]])
# data set up
data['postid'] = list(range(len(data)))
data[userid_col] = data[userid_col].astype(str)

# CREATE GEOM LIST
geomlist = create_geomlist(data, long_col, lat_col)

# CREATE GEODATAFRAME
geodata = gpd.GeoDataFrame(data)
geodata['geometry'] = geomlist
geodata.crs = CRS.from_epsg(4326)

# Geodata path
geodata_path = os.path.join(homefolder, 'app_data/geodata')
if not os.path.exists(geodata_path):
    os.makedirs(geodata_path)

geodata_filename = os.path.join(geodata_path, 'some_geodata.shp')

geodata.to_file(geodata_filename)

map_button = st.button('Show on map')

try:
    if map_button:
        st.map(geodata)
        info = st.expander('Info')
        # st.dataframe(data.style.highlight_max(axis=0))
        info.write('- {} posts'.format(len(data)))
        info.write('- {} unique users'.format(len(data[userid_col].unique())))
        info.write('- ({}) to ({})'.format(data[time_col].min(), data[time_col].max()))

except:
    st.write('data must contain columns with name lon or longitude')
    pass

# 2. ______________________UPLOAD  REGIONS LAYER_________________________
st.header('2. Upload your regions layer for spatial joining')

# layer folder
region_folder = os.path.join(homefolder, 'regions_layer')
if not os.path.exists(region_folder):
    os.makedirs(region_folder)

# Layer path
layer_list = glob.glob(os.path.join(homefolder, 'regions_layer/*shp'))

layername_list = [os.path.basename(file) for file in layer_list]

st.write('Data must be in **.shp** and in **CRS WGS-84**')
regions_layerbox = st.selectbox('Files in <regions_layer> folder', options=layername_list)

try:

    regions_geodata = read_geodata(regions_layerbox)


    regionsinfo = st.expander('Info')
    regionsinfo.write('- {}'.format(regions_geodata.crs.name))

except:
    pass

# 3. ______________________SET UP ARCPY ENVIRONMENT_________________________

st.subheader('3. Optimize spatial join with ArcGIS Pro environment')

arcpy_form = st.form('arcpyform')
arc_env = arcpy_form.text_input('URL of your Arcpy 3.6 enviroment')
arcpy_submit = arcpy_form.form_submit_button('Start spatial join')

# Enrichment process Set Up
arcenv_path = os.path.join(arc_env, 'python.exe')
gdb_filepy = os.path.join(homefolder, 'arcpy\optispatialjoin.py')

workspace = os.path.join(homefolder, 'arcpy_env.gdb')

regions_path = os.path.join(homefolder, 'regions_layer\{}'.format(regions_layerbox))
regions_name = os.path.basename(regions_path)

optiss_demo_datapath = os.path.join(workspace, 'demo_data\optiss_demo_data.shp')

if os.path.isdir(optiss_demo_datapath):
    st.balloons()
    st.success('Social media data successfully enriched!')
else:
    pass

if arcpy_submit:
    st.balloons()
    os.system(r'{} {} {}'.format(arcenv_path, gdb_filepy, regions_name))













# END
