from tesspy import Tessellation
import pandas as pd
from ..utils.gpd_file_process import FileHandle as fh

class FeaturesOfInterest(Tessellation):
    # BASE LEVEL or(TSYSTEM
    def __init__(self, city_name, zoom_level=19) -> None:
        self.city_name = city_name
        self.zoom_level = zoom_level
        super().__init__(self.city_name)
        self.squares_tessellation()
    
    def polygon(self):
        self.area_polygon = self.get_polygon()


    
    def squares_tessellation(self):
        self.square_grid = self.squares(self.zoom_level)            

    def road_of_interest(self,degree,func_arg='sum'):
        self.degree = degree
        self.func_arg = func_arg
        self.road_gpd_list= []
        #Try to catch error
        self.road_list = super.osmtag
        for road in self.road_list


    def area_of_interest(self,osm_tag,func_arg='sum'):
        self.osm_tag = osm_tag
        self.func_arg = func_arg
        
        try:
            pass
            self.building_footprint = load_gdf():
        except:
            self.ffm_building_footprint_raw = ox.geometries.geometries_from_polygon(self.area_polygon.iloc[0][1], self.osm_tag)
            self.overlay_builder(geom_arg='area')
            self.map_creator(self.func_arg)

    def overlay_builder(self, geom_arg='area'):
        self.square_grid[geom_arg] = 0  
        self.footprtin_raw = self.footprtin_raw.droplevel(0)
        self.footprtin_raw = self.footprtin_raw[self.footprint_raw.geom_type != 'Point']
        self.area_overlay = self.square_grid.overlay(self.footprtin_raw, how='difference')

    def map_creator(self):
        self.square_grid['id']=self.square_grid.index
        self.data_merged = gpd.sjoin(self.area_overlay, self.square_grid, how="inner",predicate='within')
        self.area_df = self.data_merged.groupby('id').agg(self.func_arg)
        self.final_gpd = pd.merge(self.square_grid, self.area_df, on='id', how='outer', indicator=False)

    def road_of_interest(self):
        self.
        

    

