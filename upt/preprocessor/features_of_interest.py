from tesspy import Tessellation
import geopandas as gpd
import pandas as pd
import osmnx as ox
import rasterio as rio
import rioxarray
import numpy as np
from functools import reduce


from ..utils.file_handle import FileHandle

class FeatureOfInterest(Tessellation):
    def __init__(self,city_name,crs,zoom_level=14,save_file = True,):
        ox.settings.timeout = 900
        self.city_name = city_name
        self.set_crs = crs
        
        self.zoom_level = zoom_level
        self.save_file = save_file
        super().__init__(self.city_name)
        
        self.city_config()
        self.city_path = f"{self.city_id}_{self.city_name}"
        self.fh = FileHandle(self.city_path)
        self.make_grid()
    
    def city_config(self):
        self.city_id = self.get_polygon().iloc[0][0]
        self.area_polygon = self.get_polygon().iloc[0][1]
        self.shelter_factor = {'yes':0.25 ,'residential':0.5, 'commercial': 0.5, 'retail':0.75, 'office':0.75, 'industrial': 0.75}
        self.no_fly_factor = {''}
          
    def make_grid(self):
        
        self.grid_file_name = f"{self.city_name}_sqr_{self.zoom_level}"
        grid_file_name = f"{self.grid_file_name}.gdffile"
        
        if self.fh.is_file_exist(grid_file_name,self.fh.city_dir,):
            print("loaded")
            self.square_grid = self.fh.load_gdf(self.grid_file_name, self.fh.city_dir)
        else:
            self.square_grid = self.squares(self.zoom_level)
            print("unload")
            if self.save_file:
                print("saved")
                self.fh.save_gdf(self.square_grid,self.grid_file_name,self.fh.city_dir)
        self.area_grid = self.square_grid.loc[0, 'geometry'].area
        
    def area_of_interest(self,osm_tag,func_arg='sum',geom_arg='area',verbose=False):
        self.osm_tag = osm_tag
        self.func_arg = func_arg
        self.geom_arg = geom_arg
        self.make_grid()
        
        self.overlay_file_name = f"{self.city_name}_overlay_{list(self.osm_tag.keys())[0]}_{list(self.osm_tag.values())[0]}"
        overlay_file_name = f"{self.overlay_file_name}.gdffile"
        if self.fh.is_file_exist(overlay_file_name, self.fh.feature_dir):
            if self.geom_arg == 'area':
                print("loaded gdf")
                self.area_overlay = self.fh.load_gdf(self.overlay_file_name, self.fh.feature_dir)
            elif self.geom_arg == 'length':
                self.area_overlay = self.fh.load_gdf(self.overlay_file_name, self.fh.road_dir)
                
        else:
            self.footprint_raw = ox.geometries.geometries_from_polygon(self.area_polygon, self.osm_tag)
            self.overlay_builder(geom_arg=self.geom_arg)
            if self.save_file:
                if self.geom_arg == 'area':
                    print("saved gdf")
                    self.fh.save_gdf(self.area_overlay,self.overlay_file_name,self.fh.feature_dir)
                if self.geom_arg == 'length':
                    self.fh.save_gdf(self.area_overlay,self.overlay_file_name,self.fh.road_dir)
                
        self.map_creator()
        return(self.final_gpd)
 
    def mul_area_of_interest(self,osm_tag_list,func_arg='sum',geom_arg='area',verbose=False):
        self.osm_tag_list = osm_tag_list
        self.func_arg = func_arg
        self.geom_arg = geom_arg
        self.area_list_gdf = []
        column_list = ['geometry']
        
        for osm_tag in self.osm_tag_list:
            osm_dict = osm_tag
            area_gdf = self.area_of_interest(osm_dict)
            attr_name = list(osm_dict.items())[0]
            column_name = f"{attr_name[0]}_{attr_name[1]} {geom_arg}"
            column_list.append(column_name)
            area_gdf.rename(columns = {geom_arg:column_name}, inplace = True)
            self.area_list_gdf.append(area_gdf)

        self.mul_area_gpd = reduce(lambda x, y: pd.merge(x, y, on = 'geometry'), self.area_list_gdf)
        self.mul_area_gpd = self.mul_area_gpd[column_list]
        return(self.mul_area_gpd)
        
    def road_of_interest(self,detail_deg, func_arg='sum',verbose=False):
        if detail_deg is None:
            highwaytypes = self.osm_highway_types()
        elif type(detail_deg) is int and detail_deg <= len(self.osm_highway_types()):
            highwaytypes = self.osm_highway_types()[:detail_deg]
        else:
            raise ValueError("Please insert a valid detail degree: None or int")
        
        self.road_list_gdf = []
        
        for road_type in highwaytypes:
            osm_dict = {'highway':road_type}
            road_gdf = self.area_of_interest(osm_dict, geom_arg='length')
            self.road_list_gdf.append(road_gdf)
        
        return(self.road_list_gdf)
    
    def overlay_builder(self, geom_arg='area'):
        if geom_arg =='area':
            self.footprint_raw = self.footprint_raw[self.footprint_raw.geom_type != 'Point']
            self.footprint_raw = self.footprint_raw[self.footprint_raw.geom_type != 'LineString']
            self.area_overlay = self.square_grid.overlay(self.footprint_raw, how='intersection')
            self.area_overlay[geom_arg]=self.area_overlay.to_crs(self.set_crs).area
        if geom_arg =='length':
            self.footprint_raw = self.footprint_raw[self.footprint_raw.geom_type != 'Point']
            self.area_overlay  = self.footprint_raw.copy()
            self.area_overlay[geom_arg]=self.area_overlay.to_crs(self.set_crs).length

        self.map_creator()
    
    def p_density(tif_file):
        with rio.Env():
            with rio.open(tif_file) as src:
                crs = src.crs

                # create 1D coordinate arrays (coordinates of the pixel center)
                xmin, ymax = np.around(src.xy(0.00, 0.00), 9)  # src.xy(0, 0)
                xmax, ymin = np.around(src.xy(src.height-1, src.width-1), 9)  # src.xy(src.width-1, src.height-1)
                x = np.linspace(xmin, xmax, src.width)
                y = np.linspace(ymax, ymin, src.height)  # max -> min so coords are top -> bottom

                # create 2D arrays
                xs, ys = np.meshgrid(x, y)
                zs = src.read(1)

                # Apply NoData mask
                mask = src.read_masks(1) > 0
                xs, ys, zs = xs[mask], ys[mask], zs[mask]

        data = {"X": pd.Series(xs.ravel()),
                "Y": pd.Series(ys.ravel()),
                "Z": pd.Series(zs.ravel())}
        
        pop_df = pd.DataFrame(data=data)
        geometry = gpd.points_from_xy(pop_df.X, pop_df.Y)
        pop_gdf = gpd.GeoDataFrame(pop_df, crs=crs, geometry=geometry)
        pop_gdf['population'] = 1 
        pop_gdf.to_crs("EPSG:3857", inplace=True)
        return(pop_gdf)

    def map_creator(self):
        self.square_grid['id']=self.square_grid.index
        
        self.data_merged = gpd.sjoin(self.area_overlay, self.square_grid, how="inner",predicate='within')
        self.data_merged['height'] = self.data_merged['height'].astype(float)
        self.data_merged['building'] = self.data_merged['building'].map(self.shelter_factor).fillna(0)
        self.data_merged['no fly zone'] = np.where(self.data_merged[['aeroway','military']].notnull().any(axis=1), -1, 0)
        self.data_merged = self.data_merged.rename(columns={'building': 'shelter factor'})
        
        self.area_df = self.data_merged.groupby('id')[self.geom_arg].agg(self.func_arg)
        self.height_df = self.data_merged.groupby('id')['height'].agg('max')
        self.type_df = self.data_merged.groupby('id')['shelter factor'].agg(lambda x: x.mode()[0])
        self.no_fly_df = self.data_merged.groupby('id')['no fly zone'].agg('min')
        
        self.merged_area_df = pd.merge(self.square_grid, self.area_df, on='id', how='outer', indicator=False)
        self.merged_type_df = pd.merge(self.merged_area_df, self.type_df, on='id', how='outer', indicator=False)
        self.merged_no_fly_df = pd.merge(self.merged_type_df, self.no_fly_df, on='id', how='outer', indicator=False)
        self.final_gpd = pd.merge(self.merged_no_fly_df, self.height_df, on='id', how='outer', indicator=False)
        
        self.final_gpd.fillna(0,inplace=True)
        self.final_gpd.to_crs("EPSG:3857", inplace=True)
        print(self.final_gpd.crs)
        
        if self.save_file:
            calculated_file_name = f"{self.city_name}_calculated_{list(self.osm_tag.keys())[0]}_{list(self.osm_tag.values())[0]}"
            if self.geom_arg == 'area':
                    self.fh.save_gdf(self.final_gpd,calculated_file_name,self.fh.feature_dir)
            if self.geom_arg == 'length':
                self.fh.save_gdf(self.final_gpd,calculated_file_name,self.fh.road_dir)
        
    def pop_join(gdf1, gdf2):
        dfsjoin = gpd.sjoin(gdf1, gdf2) #Spatial join Points to polygons
        dfpivot = pd.pivot_table(dfsjoin,index='id',aggfunc={'population':np.sum})
        pop_join_gdf = gdf1.merge(dfpivot, how='left', on='id')
        # pop_join_gdf['population'] = pop_join_gdf['population']/gdf1.iloc[0]['geometry'].area
        pop_join_gdf['population'] = pop_join_gdf['population']
        
        return(pop_join_gdf)
        