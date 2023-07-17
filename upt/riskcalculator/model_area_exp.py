import geopandas as gpd
import numpy as np

from upt.aircraft.base_impact_model import BaseImpactModel
from upt.riskcalculator.sjoin_mask import sjoin_mask

class AreaExpose:
    def __init__(self,gpd, ac_profile, min_threshold=50, fatal_threshold= 68):
        self.alpha = min_threshold
        self.beta = fatal_threshold
        self.gpd = gpd
        self.ac_profile = ac_profile
        self.flight_level = ac_profile['flight_lv']
        
    def run_function(self):
        self.pre_fatality_score()
        self.impact_score()
        self.flight_level_score()
        return(self.gpd)
        
    def fatality_eq(self,ps):
        fatality_score = (np.sqrt(self.alpha/self.beta)*(1/self.beta)**(0.25*ps))
        return(fatality_score)
    
    def impact_score(self):
        drone_radius = self.ac_profile['diagonal size']/2
        glide_slope_angle = np.deg2rad(self.ac_profile['glide descent angle']) 
        self.Aexp = 2*(0.23 + drone_radius)*(1.74/np.tan(glide_slope_angle))+np.pi*((0.23+drone_radius)**2)
        self.gpd['impact score'] = self.gpd['population']*self.Aexp
    
    def pre_fatality_score(self):
        self.gpd['pre fatality'] = self.gpd['shelter factor'].apply(lambda x:  self.fatality_eq(x))
        
    def flight_level_score(self):
        self.gpd['fly level score'] = np.where(self.gpd['height'] > self.flight_level, -1, 0)
    
    def sum_descent(self, ac_profile, descent_type):
        self.sample_number = 10000
        idx = np.arange(0, self.gpd.shape[0])
            
        ballistic_trajectory = BaseImpactModel("ballistic", ac_profile, self.gpd.crs, self.sample_number)
        ballistic_mask = ballistic_trajectory.run_model()
        print("Running Ballistic Model")
        self.ballistic_risk = sjoin_mask(idx,ballistic_mask,self.gpd)
        
        glide_trajectory = BaseImpactModel("glide", ac_profile, self.gpd.crs, self.sample_number)
        glide_mask = glide_trajectory.run_model()
        print("Running Glide Model")
        self.glide_risk = sjoin_mask(idx,glide_mask,self.gpd)
        
        parachute_trajectory = BaseImpactModel("parachute", ac_profile, self.gpd.crs, self.sample_number)
        parachute_mask = parachute_trajectory.run_model()
        print("Running Parachute Model")
        self.parachute_risk = sjoin_mask(idx,parachute_mask,self.gpd)
        
        flyaway_trajectory = BaseImpactModel("fly_away", ac_profile, self.gpd.crs, self.sample_number)
        flyaway_mask = flyaway_trajectory.run_model()
        print("Running flyaway_mask Model")
        self.flyaway_risk = sjoin_mask(idx,flyaway_mask,self.gpd)
        
        self.risk_total = np.sum([self.ballistic_risk, self.glide_risk, self.flyaway_risk], axis=0)
        return(self.applied_descent())
        
        
    def applied_descent(self):
        self.result_df = self.gpd.copy()
        #Applying mtbf = 100
        self.result_df['fatality risk total'] = self.risk_total/100
        return(self.result_df)
    
        
    def total_risk_score(self):
        self.risk_final = self.result_df.copy()
        self.risk_final['fly level score'] = np.where(self.risk_final['fly level score'] < 0, np.inf, 1)
        self.risk_final['no fly zone'] = np.where(self.risk_final['no fly zone'] < 0, np.inf, 1)
        self.risk_final['total risk'] = self.risk_final[['impact score', 'no fly zone', 'fly level score','fatality risk total']].prod(axis=1)
        self.risk_final['risk non inf'] = self.risk_final[['impact score','fatality risk total']].prod(axis=1)
        return(self.risk_final)
                                             
                                             
                                             
        
    
    