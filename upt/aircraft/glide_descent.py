from scipy. 
import numpy as np


class GlideDescent:
    def __init__(self,aircraft_config) -> None:
        self.coeff_drag = coeff_drag
        self.coeff_lift = coeff
        self.frontal_area = frontal_area
        self.phys_config()

    def phys_config(self):
        self.g = 9.81
        self.rho_sl = 1.225
        self.pressure_sl = 1.01000

    def monte_carlo(self,function):
        self.N_iteration = 1000
        from sci
    