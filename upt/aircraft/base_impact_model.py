import pandas as pd
import geopandas as gpd
import numpy as np

import ballistic_model

class base_impact_model:
    def __init__(self, model, ac_profile, crs, n_sampling = 1000):
        self.model_type = model
        self.crs = crs
        self.n_sampling = n_sampling
        self.ac_profile = ac_profile
        self.get_function()
    
    def get_function(self):
        if self.model_type == "ballistic":
            self.model_func = ballistic_model
        if self.model_type == "glide":
            pass
    
    def run_model(self):
        self.impact_point = self.model_func(self.n_sampling, self.ac_profile)
        self.binning()
        self.array_to_gpd()
        self.pd_to_gpd()
        return(self.mask_gdf)
    
    def run_unbinned_model(self):
        self.impact_point = self.model_func(self.n_sampling, self.ac_profile)
        self.binning()
        return(self.historgram )
    
    def binning(self):
        bins = [np.linspace(self.impact_point.min(), self.impact_point.max(), 10), np.linspace(self.impact_point.min(), self.impact_point.max(), 10)]
        histogram, x_bin, y_bin  = np.histogram2d(self.impact_point[0], self.impact_point[1], bins=bins)
        self.historgram = histogram
        
        self.n_point_map = {}
        self.locmap_map = {}
        self.n_point_map.setdefault("N_points", [])
        self.locmap_map.setdefault("x_loc", [])
        self.locmap_map.setdefault("y_loc", [])
        for ith, _ in enumerate(histogram):
            for jth, point in enumerate(histogram[ith]):
                self.n_point_map['N_points'].append(point)
                self.locmap_map['x_loc'].append(x_bin[ith])
                self.locmap_map['y_loc'].append(y_bin[jth])
                
    def array_to_gpd(self):
        self.n_point_df = pd.DataFrame(self.n_point_map)
        self.locmap_df = pd.DataFrame(self.locmap_map)
        self.mask_df = self.n_point_df.join(self.locmap_df)
        
    def pd_to_gpd(self):
        self.mask_gdf = gpd.GeoDataFrame(self.mask_df.copy(), geometry=gpd.points_from_xy(self.mask_df['x_loc'], self.mask_df['y_loc']))
        self.mask_gdf.drop(['x_loc','y_loc'], axis=1, inplace = True)

        #Dividde N_point by sample size
        self.mask_gdf['N_points'] = self.mask_gdf['N_points']/self.n_sampling
        self.mask_gdf = self.mask_gdf.set_crs(self.crs)
