import geopandas as gpd
import numpy as np
from shapely.geometry import LineString

def convert_linestring(way_path, crs):
    line_shape = LineString(way_path)
    line_gdf = gpd.GeoDataFrame(geometry=[line_shape])
    line_gdf.set_crs(crs, inplace=True)
    return(line_gdf)
    
def gaussian_average(way_path, crs):
    x, y = (way_path[:,0],way_path[:,1],)
    smooth_y=ndimage.gaussian_filter(y,2)
    way_smooth = np.column_stack((x,smooth_y))
    return(convert_linestring(way_smooth, crs))

def non_smooth(way_path, crs):
    x, y = (way_path[:,0],way_path[:,1],)
    way_nonsmooth = np.column_stack((x,y))
    return(convert_linestring(way_nonsmooth, crs))
