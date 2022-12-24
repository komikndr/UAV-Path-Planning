import geopandas as gpd
import concurrent.futures

def sjoin_mask(array_index, mask, gdf):
    def sjoin_risk_sum(array_index):
        mask_translate = mask.copy()
        mask_translate['geometry'] = mask.translate(gdf.iloc[array_index][0].centroid.x,gdf.iloc[array_index][0].centroid.y)
        sjoin_gp = gpd.sjoin(gdf, mask_translate)
        risk = sjoin_gp['N_points'].multiply(sjoin_gp['area']).sum()
        return(risk)
    
    result_list = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(sjoin_risk_sum, idx)
    
        for result in results:
            result_list.append(result)

    return(result_list)