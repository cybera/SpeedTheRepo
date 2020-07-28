import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as mpl

class NetworkHeatmaps():
    '''
    Simple Python class in order to process network data from statistics canada and create heatmaps 
    to understand the distribution of high-speed internet access across Canada. 
    '''

    def __init__(self, dfcan, dfmap, folder = "fig/", suffix = "_heat", save=False, points = 1000):
        '''
        dfcan -> geopandas dataframe of the shapefile of canada you wish to use
        dfmap -> "NBD_Roads_Shapefile/NBD_ROAD_SPEEDS.shp" from statistics canada
        
        all others are managed automatically, but what they are is outlined below 
        res_difference -> The dataframe used to create the patches to hide data not 
                          part of the province/canada
        xi, yi, zi     -> x, y, and z points for the heatmap 
        folder         -> folder to save images
        suffix         -> suffix behind images, if desired
        save           -> true/false if you're saving images or not
        points         -> number of points for the interpolation
        for_map        -> dataframe for the heatmap 
        '''

        self.dfcan = dfcan
        self.dfmap = dfmap
        self.res_difference = None
        self.xi = None
        self.yi = None
        self.zi = None
        self.folder = folder
        self.suffix = suffix
        self.save = save
        self.points = points
        self.for_map = None
        
    def maxAvail(self, row):
        '''
        Python function to determine the maximum available speed on a given network
        segment. Probably a faster way to do this as I've not really
        vectorized anything here
        '''
        if row.Avail_50_1 == 1:
            return 50
        if row.Avail_25_5 == 1:
            return 25
        if row.Avail_10_2 == 1:
            return 10
        if row.Avail_5_1_ == 1:
            return 5
        else:
            return 0
        
    def pointExtractor(self, df):
        '''
        This function converts the LineSegment pieces of the network data
        to raw latitude and longitude coordinate
        '''
        pdict = {'lat':[], 'long':[], 'speed':[]}
        for row in df.iterrows():
            for tup in row[1]['points']:
                pdict['lat'].extend([tup[1]])
                pdict['long'].extend([tup[0]])
                pdict['speed'].extend([row[1]['max_speed']])
        return pd.DataFrame(pdict)
    
    def prepData(self):
        '''
        Preps the data for heatmaps. This whole process is very slow, and 
        I should probably spend some time speeding this code up
        '''
        
        try: 
            self.dfmap['max_speed']
            print("Max speed already calculated")
        except KeyError:
            print("Calculating max speed")
            self.dfmap['max_speed'] = self.dfmap.apply(self.maxAvail, axis = 1)
        try:
            self.dfmap['points']
            print("Points already calculated")
        except KeyError:
            print("Converting to lat/long points")
            self.dfmap['points'] = self.dfmap.apply(lambda x: [y for y in x['geometry'].coords], axis=1)
        if not isinstance(self.for_map, type(None)):
            print("Map Exists")
        else:
            print("Point-Stracting")
            self.for_map = self.pointExtractor(self.dfmap)
        print("Performing Interpolation")
        self.makeInterpolation()
    
    def makePatch(self, df):
        '''
        This function generates the patch to hide things that don't 
        fall within the shapefiles we wish to use
        '''
        # Super rough bounding rectangle around canada
        outer = Polygon(((-150, 35),(-150,100),(-50, 100),(-50,35)))
        dfPatch = gpd.GeoSeries(outer)
        dfPatch = gpd.GeoDataFrame(dfPatch)
        dfPatch.columns = ['geometry']
        self.res_difference = gpd.overlay(dfPatch, df, how='difference')
        
    
    def makeInterpolation(self):
        '''
        This function creates an interpolation between all our data points
        '''
        y = self.for_map['lat']
        x = self.for_map['long']
        z = self.for_map['speed']

        self.xi = np.linspace(x.min(), x.max(), self.points)
        self.yi = np.linspace(y.min(), y.max(), self.points)

        self.zi = griddata((x, y), z, (self.xi[None,:], self.yi[:,None]), method='linear', rescale=True)
        self.zi[self.zi > 50 ] = 50
    
       
    def makePlot(self, data, patch, box = None, title=None, file=None, save=False):
        '''
        Creates the plots
        '''
        
        fig, ax = plt.subplots(figsize=(15,15))
        ax.axis('scaled')
        bound = np.linspace(0, 50, 13)
        CS = ax.contourf(self.xi,self.yi,self.zi,
                         cmap=plt.cm.jet, vmin=0, vmax=50, 
                         alpha=.5, levels=bound)
        
        self.makePatch(patch)
        self.res_difference.plot(ax=ax, color = 'white')
        
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)

        cbar = fig.colorbar(CS, cax=cax)
        cbar.set_ticklabels([0, 8, 16, 25, 33, 41,50])
        
        cbar.set_label("(Smoothed) Max Mbps Download", size = 16)
        ax.set_xlabel("Longitude", size = 24)
        ax.set_ylabel("Latitude", size = 24)

        cbar.set_label("(Smoothed) Max Mbps Download", size = 16)
        ax.set_xlabel("Longitude", size = 24)
        ax.set_ylabel("Latitude", size = 24)

        if box:
            ax.set_xlim([patch.bounds['minx'].values[0] -0.5, patch.bounds['maxx'].values[0] +0.5])
            ax.set_ylim([patch.bounds['miny'].values[0] -0.5, patch.bounds['maxy'].values[0] +0.5])
        if title:
            ax.set_title(title, size = 20)

        if save:
            print('saving to', file)
            plt.savefig(file, dpi=300)
        plt.show()
        
        
   
    def provincePlots(self):
        ''' If desired, this automates makeing plots
        for individual provinces'''

        for prov in self.dfcan['PRENAME'].unique():
            print("Starting plot for", prov)
            local = self.dfcan[self.dfcan['PRENAME'] == prov]
            self.makePlot(self.for_map, local, save=True, title=prov,
                           file = self.folder + str(prov) + self.suffix + ".png")
            

    def framePlot(self, df, title=None, save=False, file = "customplot.png"):
        '''
        Plots anything you want, just  need to pass it a geopandas dataframe
        defining the shapefile of your data
        '''
 
        self.makePlot(self.formap,df, save=save, title=title, file=file)

        
        
    
    
        
        