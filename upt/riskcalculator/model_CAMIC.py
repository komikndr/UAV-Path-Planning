def model_CAMIC(gdf, attr_weight_dict, feature_threshold):
    gdf = gdf.copy()
    area_threshold = feature_threshold*gdf.iloc[[0]].area[0]
    
    for attr_weight in attr_weight_dict:
        gdf[attr_weight] = gdf[attr_weight].apply(lambda x : 0 if x < area_threshold else attr_weight_dict[attr_weight])
        
    return (gdf)
    