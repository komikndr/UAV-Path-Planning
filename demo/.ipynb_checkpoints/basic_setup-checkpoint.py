from upt.preprocessor.features_of_interest import FeatureOfInterest as foi
from upt.postprocessor.a_star import AStar
from upt.utils.geo_utils import line_smoothing as lsp

import matplotlib.pyplot as plt


depok_obj = foi('Depok',crs=3857,zoom_level=17)
depok_school = depok_obj.area_of_interest({'amenity':'school'})


depok_star = AStar(depok_school,'area',crs=depok_school.crs)
depok_path = depok_star.run_instance(3,1000)
way_marker = depok_star.create_line()
way_path = lsp(way_marker[:,0],way_marker[:,1],)

ax = depok_school.plot(column="amenity school_area",cmap='afmhot')
plt.plot(way_path[:,0], way_path[:,1],color='blue')
plt.show()