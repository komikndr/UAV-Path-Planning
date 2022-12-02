from upt.preprocessor.features_of_interest import FeatureOfInterest as foi
from upt.postprocessor.a_star import AStar
from upt.utils.geo_utils import line_smoothing as lsp
from upt.utils.file_handle import FileHandle

import matplotlib.pyplot as plt

fh = FileHandle("14525364_Depok")
depok_school = fh.load_gdf("Depok_calculated_amenity_school",fh.feature_dir)

depok_star = AStar(depok_school,'area',crs=depok_school.crs)
depok_path = depok_star.run_instance(3,1000)
way_marker = depok_star.create_line()
way_path = lsp(way_marker[:,0],way_marker[:,1],)
# print(way_marker)

ax = depok_school.plot(column="amenity school_area",cmap='afmhot')
plt.plot(way_path[:,0], way_path[:,1],color='blue')
plt.show()
