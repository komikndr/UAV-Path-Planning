import os

def mkdir_upt(folder_name='city_data'):
    path_file = os.getcwd()
    parent_path = (f"{path_file}\{folder_name}")
    os.mkdir(parent_path)
    dir_list = ['city_dir','road_dir','feature_dir']
    for directory in dir_list:
        os.mkdir(f"{parent_path}\{directory}")