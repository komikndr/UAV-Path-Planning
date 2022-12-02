from upt.preprocessor.features_of_interest import FeatureOfInterest as foi
from upt.postprocessor.a_star import AStar
from upt.utils.geo_utils import line_smoothing as lsp

import matplotlib.pyplot as plt

depok_obj = foi('Depok',crs=3857,zoom_level=17)
feature_list = [{"amenity":"school"},{"amenity":"cafe"}]
depok_school = depok_obj.mul_area_of_interest(feature_list)

print(depok_school)