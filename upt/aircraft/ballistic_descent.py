from scipy. 
import numpy as np


class BallisticDescent:
    def __init__(self,coeff_drag,frontal_area) -> None:
        self.coeff_drag = coeff_drag
        self.frontal_area = frontal_area
        self.physs()
    
    def phys_config(self):
        self.g = 9.81
        self.rho_sl = 1.225
        self.pressure_sl = 1.01000

    def monte_carlo(self,function):
        self.N_iteration = 1000
        from sci
        