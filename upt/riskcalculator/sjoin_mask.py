import geopandas as gpd
import concurrent.futures
import numpy as np

def sjoin_mask(array_index, mask, gdf):
    def sjoin_risk_sum(array_index):
        mask_translate = mask.copy()
        mask_translate['geometry'] = mask.translate(gdf.iloc[array_index][0].centroid.x,gdf.iloc[array_index][0].centroid.y)
        sjoin_gp = gpd.sjoin(gdf, mask_translate)
        impact_exponent = sjoin_gp['E_imp']**(0.25*sjoin_gp['shelter factor'])                        
        fatality = 1/(1+(sjoin_gp['pre fatality'].multiply(impact_exponent)))
        risk = sjoin_gp['N_points'].multiply(fatality).sum()
        # risk = sjoin_gp[attr_columns].prod().sum()
        return(risk)
    
    result_list = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(sjoin_risk_sum, array_index)
    
        for result in results:
            result_list.append(result)
    
    # result_df = gdf.copy()
    # result_df['risk'] = result_list
    # return(result_df)
    return(result_list)



