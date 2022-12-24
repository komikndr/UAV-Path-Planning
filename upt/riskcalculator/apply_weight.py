import geopandas as gpd
import numpy as np

#GDF MUST PURELY FLOAT OR INT NOT GEOMETRY POINT
#Linear Risk Function
def linear_weight(gdf,weight_list):
    for col_index, col_name in enumerate(gdf):
        gdf[col_name] = gdf[col_name].apply(lambda x : x* weight_list[col_index])
        gdf['risk'] = gdf.sum(axis=1)
    return(gdf)

#Custom Risk Function
def custom_function(gdf,c_func):
    for col_index, col_name in enumerate(gdf):
        gdf[col_name] = gdf[col_name].apply(lambda x : c_func[col_index](x))
        gdf['risk'] = gdf.sum(axis=1)
    return(gdf)

#Constant Risk Function
def const_func(gdf):
    gdf['risk'] = gdf.sum(axis=1)
    return(gdf)

 