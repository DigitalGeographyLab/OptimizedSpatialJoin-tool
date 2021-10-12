# OptiSS 🧐 - Tool for optimizing spatial joining of big social media data

The OptiSS Tool is a local app user friendly (hopefully =]) that optimize the spatial joining of **social media posting history** with Political-Administrative Division datasets (i.e. countries).

The outcome is an enriched **optiss demo data.shp** that contains the attribute of administrative unit for each social media post location. You can find instructions about OptiSS in the next links:

- [How does OptiSS work?](https://github.com/DigitalGeographyLab/OptimizedSpatialJoin-tool#how-does-optiss-work)
- [How to use OptiSS?](https://github.com/DigitalGeographyLab/OptimizedSpatialJoin-tool#how-to-use-optiss)
- [How to set up OptiSS?](https://github.com/DigitalGeographyLab/OptimizedSpatialJoin-tool#how-to-set-up-optiss)

For some experienced users that want to implement OptiSS algorithm in their own workflow you can do it using the script `manual_optiss.py` in the folder `arcpy`. You can follow directly the short instruction in the next link: 

- [Implementation of OptiSS in your workflow](https://github.com/DigitalGeographyLab/OptimizedSpatialJoin-tool#manual-usage---implementation-in-your-own-workflow)

## How does OptiSS work?

OptiSS tool optimize the spatial joining of social media posting history with a regions layer.

With OptiSS the spatial joining is faster than using manually ArcGIS Pro console. The reason why is because this code makes efficient the process by optimizing it in two parts: ***1. Spatial join of Inland posts***, and ***2. Spatial join of Outland posts***. Commonly, the Outland posts consumes extra computational power (Geodetic Spatial Join) and takes time if you run the whole dataset in console. 

OptiSS tool was tested with a **twitter posting history** dataset at global level with 50244 posts of 500 unique users in 9 years period. You can take a look to this dataset in the section [How to use OptiSS?](https://github.com/DigitalGeographyLab/OptimizedSpatialJoin-tool#how-to-use-optiss). The efficiency in the spatial join process with OptiSS optimized the time in 64.4% in comparison with ArcGIS pro console. You can see it in the next chart:

![test chart](png/test-chart.png)

## How to use OptiSS?

OptiSS tool usage is explained in this example with a **twitter posting history** dataset at global level with 50244 posts of 500 unique users in 9 years period.  Next, you will see some details about the example and the steps that needs to be followed in OptiSS usage.

### Datasets

You need to save your own files in folders: `app_data`, and `regions_layer`. You will find a [twitter sample dataset](https://github.com/DigitalGeographyLab/OptimizedSpatialJoin-tool/tree/main/app_data) in this repository containing 1000 posts from 4 unique users. But for this example OptiSS used next datasets:

- **twitter posting history.csv** dataset at global level with 50244 posts, of 500 unique users, in 9 years posting history, delimited by semicolon. In folder `app_data`

- **global_regions_fixed_wgs84.shp** (Database of [Global Administrative Areas](https://gadm.org/) - Internal use file). In folder `regions_layer`
 
### 1. Uploading social media posting history

OptiSS starts with a short explanation and includes the link to this section. Then the first part is to upload your social media dataset. You first select your file stored in folder `app_data` and specify the columns of *timestamp*, *longitude*, *latitude*, and *user id*. You will notice that data is loaded when the local app ends *running process* at the right-upper corner. Then you press the button *Show on map* if prefered. It will look like this:

![1. upload data](png/optiss1.png)

### 2. Uploading regions layer for spatial joining

Then, you select your file stored in folder `regions_layer`. Be sure you stored in *.shp* format and in crs *WGS 84*. It will look like this:

![2. upload regions data](png/optiss2.png)


### 3. Optimize spatial join with ArcGIS Pro environment

Finally, you have to specify the URL where the *Arcpy environment* is stored. The recommendation is to do a copy of original environment and paste it from ArcGIS Pro installation folder to the Anaconda environments folder. The instructions can be found in the [arcpy_url.txt](https://github.com/DigitalGeographyLab/OptimizedSpatialJoin-tool/blob/main/arcpy_url.txt) file in this repository. OptiSS will look like:

![3. arcpy environment](png/optiss3.png)

### Results
Once the process started correctly with Arcpy environment you will notice ballons on the screen. This is a good sign. Finally, the result is an *optiss demo data.shp* file stored in a new folder called `optiss_result`. At the moment you open the result you will notice how the social media posts contain the attributes of the region layer including the ones out of the main land. The next image shows some post out of land between Estonia and Finland (left), and the view at EU level with country attribute (right). Click over to see it bigger:

![5 result view](png/5_result.png)

## How to set up OptiSS?

Simply, clone the repository in your computer, open the repo directory in command line, and run `streamlit run optiss-app.py`
 
Step by step:
1. Open Anaconda prompt (command line)
2. Optional. Activate your own environment with all needed libraries if they are not in base environment
3. Navigate to your the desired location to save Optiss in local disk. (i.e. `cd C:\Users\bryanval\DGL\Github\`)
4. Clone the repository by typing `https://github.com/DigitalGeographyLab/OptimizedSpatialJoin-tool.git`
5. Navigate to your repository by typing in command line `cd OptimizedSpatialJoin-tool` 
6. Run the app by typing `streamlit run optiss-app.py`

### Installing packages

1. You need to have installed in Python 3 environment:

   * streamlit `conda install -c conda-forge streamlit`
   * pandas
   * geopandas
   * pyproj
   * shapely
   * descartes `conda install -c conda-forge descartes`

2. You need to have ArcGIS pro 2.2 license (i.e. University of Helsinki license). This instructions are included in the [arcpy_url.txt](https://github.com/DigitalGeographyLab/OptimizedSpatialJoin-tool/blob/main/arcpy_url.txt) file in this repo.

   * Find the URL of the Arcpy environment 3.6. Commonly it can be found here: `C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3`
   * Then, copy the enviroment folder `arcgispro-py3` to your local folder of enviroments of Anaconda. Commonly the enviroments are located here `C:\HYapp\Anaconda3\envs\`
   * Finally, after the copy is done, the final URL is: `C:\HYapp\Anaconda3\envs\arcgispro-py3`

### Make sure everything works
 
1. Save your *social media posting history.csv* in folder `app_data` delimited by semicolons
   * Data must include columns *Longitude*, *Latitude*, *Timestamp*, *User_id*. You can change names
   * *Note*. Coordinates in WGS 84. Name the columns in example 'lat' or 'latitude' (required for visualization in app)
 
2. Set up Regions Layer
   * Save yor **Regions_layer.shp** in WGS84 in folder `regions_layer`
   
3. Check the process
   * You can supervise the process in the command line. It will start giving messages of the process
   
4. Re-start a new process
   * Recommended to erase entirely the **.gdb** and the **optiss_demo_data.shp** generated before starting a new process

## Manual usage - Implementation in your own workflow

If you are more experienced you can implement the optiss algorithm in your workflow independently. In the folder `arcpy` you will find the script ready to be used manually called ***manual_optiss.py***. You just need to set up the names of the files in the section *Parameters*. 

Then, you activate the enviroment of Arcpy 3.6 (arcgispro-py3) in Anaconda command prompt and set up the directory of the folder `arcpy`. Finally, run the line `python manual_optiss.py`

## Notes on the output

In the folder `optiss_result` you will find the enriched social media posting history as **optiss_demo_data.shp**.
You will notice that in the copied local repository in your computer there is a new **arcpy_env.gdb** that contains temporal files of the process and they are not relevant.
Note! For security there is also a copy of the result in the **arcpy_env.gdb**

## Known issues

1. While ussing the tool. Keep ArcGIS pro console closed or not using your regions file. Otherwise, it will fail the process because of **lock** (file used by other console)
2. If you want to create a new demo dataset with a second social media posting history be sure you have erased first **arcpy_env.gdb**. The tool do not do replacements. Basically, do all again if posible in a new folder.
3. When social media posting history is too big some geometries fail in creation. In that case you need to add a code line to correct geometry. Mentioned code lines are already in the scripts but not activated to make it run faster. If you encounter geometry creation problems be aware to activate this lines by erasing the **#** simbol.

## Referencing

There is no reference because the tool is not public at the moment.

