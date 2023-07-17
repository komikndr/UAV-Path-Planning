import osmnx as ox 
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
from scipy import ndimage
from geopy.geocoders import Nominatim

def line_smoothing(x,y):
    smooth_y=ndimage.gaussian_filter(y,2)
    smooth_line = np.column_stack((x,smooth_y))
    return(smooth_line)

class GeoHandler:
    def __init__(self):
        self.crs = "epsg:4326" 
    
    def geocoder(self, query):
        self.query = query
        self.coord = ox.geocoder.geocode(self.query)
        return(self.coord)
    
    def grid_select(self,coord):
        self.coord = coord
        self.coord = self.coord [::-1]
        self.point_coord = Point(self.coord)
        self.point_coord = gpd.GeoDataFrame({'col1': ['name1'], 'geometry': [Point(self.coord)]})
        self.point_coord = self.point_coord.set_crs(self.crs)
        self.gdf = self.gdf.to_crs(self.crs)
        
        node_gdf = self.gdf.sjoin(self.point_coord ,predicate='contains',how='right')
        node_id =node_gdf['index_left'][0]
        return(node_id)
    
#     def grid_select(self, coord):
#         geolocator = Nominatim(user_agent="UAV Path Finder")
#         latitude = location.latitude
#         longitude = location.longitude
    
    def node_select(self,gdf, query):
        self.gdf = gdf
        if isinstance(query,str):
            self.coord  = self.geocoder(query)
            return(self.grid_select(self.coord))
        elif isinstance(query,float):
            return(self.grid_select(query))
        elif isinstance(query,int):
            return(query)

