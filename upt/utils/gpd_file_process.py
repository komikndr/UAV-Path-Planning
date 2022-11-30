import pickle
import os 

class FileHandle:
    def __init__(self) -> None:
        self.get_cwd = os.getcwd()
        self.parent_dir = self.get_cwd.parent.parent
        self.path = path

        self.city_dir = "City File"
        self.cities_dir = os.path.join(self.parent_dir,self.city_dir)

    def is_file_exist(self, name, path_file):
        #name = Name of the file
        #path_file = folder type of file, e.g feature_dir,road_dir
        #extension = extension of file, e.g .gpd;.json;.geoJSON
        file_name = name
        file_folder_dir = os.path.join(self.cities_dir,path_file)
        file_path = os.path.join(file_folder_dir,file_name)

        return (os.path.isfile(file_path))

    def load_gdf(self, name, path_file):
        #Away with elegance, i'll do what i do
        gdf_name = f"{name}.gdffile"
        gdf_folder_dir = os.path.join(self.cities_dir,path_file)
        gdf_path = os.path.join(gdf_folder_dir,gdf_name)

        with open(gdf_path, 'rb') as gpdfile:
            return_gdf = pickle.load(gpdfile)
        return(return_gdf)

    def save_gdf(self, gdf, name, path_file):
        gdf_name = f"{name}.gdffile"
        gdf_folder_dir = os.path.join(self.cities_dir,path_file)
        gdf_path = os.path.join(gdf_folder_dir,gdf_name)

        with open(gdf_path, 'wb') as gpdfile:
            pickle.dump(gdf, gpdfile, pickle.HIGHEST_PROTOCOL)

    def load_json(json_name,path_file):
        pass

    def save_json(json_name,path_file):
        pass


