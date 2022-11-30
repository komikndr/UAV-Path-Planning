from tesspy import Tessellation
import geopandas as gpd
import pandas as pd
import osmnx as ox

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
            self.area_overlay = self.square_grid.overlay(self.footprint_raw, how='difference')
            self.area_overlay[geom_arg]=self.area_overlay.to_crs(self.set_crs).area
        if geom_arg =='length':
            self.footprint_raw = self.footprint_raw[self.footprint_raw.geom_type != 'Point']
            self.area_overlay  = self.footprint_raw.copy()
            self.area_overlay[geom_arg]=self.area_overlay.to_crs(self.set_crs).length

        self.map_creator()
        
    def map_creator(self):
        self.square_grid['id']=self.square_grid.index
        self.data_merged = gpd.sjoin(self.area_overlay, self.square_grid, how="inner",predicate='within')
        self.area_df = self.data_merged.groupby('id')[self.geom_arg].agg(self.func_arg)
        self.final_gpd = pd.merge(self.square_grid, self.area_df, on='id', how='outer', indicator=False)
        self.final_gpd.fillna(0,inplace=True)
        
        if self.save_file:
            calculated_file_name = f"{self.city_name}_calculated_{list(self.osm_tag.keys())[0]}_{list(self.osm_tag.values())[0]}"
            if self.geom_arg == 'area':
                    self.fh.save_gdf(self.final_gpd,calculated_file_name,self.fh.feature_dir)
            if self.geom_arg == 'length':
                self.fh.save_gdf(self.final_gpd,calculated_file_name,self.fh.road_dir)
        