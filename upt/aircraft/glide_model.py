import numpy as np

def glide_model(n_sampling, ac_profile, v_wind = 0 , wind_dir=0):
    wind_dir = np.deg2rad(wind_dir)
    v_wind_x = np.cos(wind_dir)*v_wind
    v_wind_y = np.sin(wind_dir)*v_wind
    glide_speed = ac_profile['glide speed']
    
    sample_points = np.random.normal(glide_speed, 3, size=(n_sampling))
    gamma = np.arctan(np.deg2rad(ac_profile['glide descent angle']))
    flight_lv = ac_profile['flight_lv']
    mass = ac_profile['mass']
    
    def glide(v_sample):
        point_list = []
        for v in v_sample:
            
            angle_degree = np.random.uniform(0,2*np.pi)
            
            radial_func_x = lambda angle : v*np.cos(angle)
            radial_func_y = lambda angle : v*np.sin(angle)
            
            vg_x = radial_func_x(angle_degree) + v_wind_x
            vg_y = radial_func_y(angle_degree) + v_wind_y
            v_magnitude = np.linalg.norm([vg_x,vg_y])
            
            flight_lv_dist = np.random.normal(flight_lv, 1)
            td = flight_lv_dist/v_magnitude*np.sin(gamma)
            
            angle_radians = np.arctan2(vg_y, vg_x)
            angle_radians = (angle_radians + 2*np.pi) % (2*np.pi)
            
            point_x = v_magnitude*td*np.cos(angle_radians)
            point_y = v_magnitude*td*np.sin(angle_radians)

            E_imp = 1/2*mass*v_magnitude**2
            point_list.append((point_x,point_y, E_imp))
        return (np.array(point_list))

    crash_point = glide(sample_points)
    crash_point = np.column_stack((crash_point))
    return(crash_point)