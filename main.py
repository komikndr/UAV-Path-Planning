from upt.preprocessor.features_of_interest import FeatureOfInterest as foi
from upt.postprocessor.AStar import AStar
import matplotlib.pyplot as plt


depok_obj = foi('Depok',crs=3857,zoom_level=17)
depok_school = depok_obj.area_of_interest({'amenity':'school'})

depok_star = AStar(depok_school,'area',crs=depok_school.crs)
depok_path = depok_star.run_instance(30,1400)
marker = depok_star.create_line()
print(len(depok_path))