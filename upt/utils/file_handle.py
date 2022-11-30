import pickle
import os 

class FileHandle:
    def __init__(self,city_id_name) -> None:
        self.get_cwd = os.getcwd()
        self.parent_dir = self.get_cwd

        self.city_data_dir = os.path.join(self.parent_dir, "city_data")
        self.city_id_dir = os.path.join(self.city_data_dir, f"{city_id_name}")
        
        self.road_dir = os.path.join(self.city_id_dir, "road_dir")
        self.city_dir = os.path.join(self.city_id_dir, "city_dir")
        self.feature_dir = os.path.join(self.city_id_dir, "feature_dir")
        
        os.makedirs(self.city_data_dir,exist_ok=True)
        os.makedirs(self.city_id_dir,exist_ok=True)
        os.makedirs(self.road_dir,exist_ok=True)
        os.makedirs(self.city_dir,exist_ok=True)
        os.makedirs(self.feature_dir,exist_ok=True)

    def is_file_exist(self, name, path_file):
        file_name = name
        file_path = os.path.join(path_file,file_name)

        return (os.path.isfile(file_path))

    def load_gdf(self, name, path_file):
        #Away with elegance, i'll do what i do
        gdf_name = f"{name}.gdffile"
        gdf_path = os.path.join(path_file,gdf_name)

        with open(gdf_path, 'rb') as gpdfile:
            return_gdf = pickle.load(gpdfile)
        return(return_gdf)

    def save_gdf(self, gdf, name, path_file):
        gdf_name = f"{name}.gdffile"
        gdf_path = os.path.join(path_file,gdf_name)

        with open(gdf_path, 'wb') as gpdfile:
            pickle.dump(gdf, gpdfile, pickle.HIGHEST_PROTOCOL)

    def load_json(json_name,path_file):
        pass

    def save_json(json_name,path_file):
        pass