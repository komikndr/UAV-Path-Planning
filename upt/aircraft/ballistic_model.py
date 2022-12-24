import numpy as np

def ballistic_model(n_sampling, ac_profile):
    sample_points = np.random.normal(15, 3, size=(n_sampling))
    mass = ac_profile['mass']
    g = ac_profile['g']
    cd = ac_profile['cd']
    flight_lv = ac_profile['flight_lv']
    
    gamma = np.sqrt(mass*g/cd)
    log2 = np.log(2)
    cd_z = cd*flight_lv
    m_per_c = mass/cd
    m_gamma = mass*gamma
    
    #Warning! Mathematically untested
    def ballistic(v_sample):
        point_list = []
        for v in v_sample:
            angle_degree = np.radians(np.random.uniform(0,360))
            ballistic_x = m_per_c*np.log(1+(v*((mass*log2+cd_z)/(m_gamma))))
            ballistic_y = m_per_c*np.log(1+(v*((mass*log2+cd_z)/(m_gamma))))
            
            radial_ballistic_func_x = lambda angle :ballistic_x*np.cos(angle)
            radial_ballistic_func_y = lambda angle :ballistic_y*np.sin(angle)
            x_point = radial_ballistic_func_x(angle_degree)
            y_point = radial_ballistic_func_y(angle_degree)
            point_list.append((x_point,y_point))
        return (np.array(point_list))

    crash_point = ballistic(sample_points)
    crash_point = np.column_stack((crash_point))
    return(crash_point)