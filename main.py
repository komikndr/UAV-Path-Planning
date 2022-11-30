from upt.preprocessor.features_of_interest import FeatureOfInterest as foi
import matplotlib.pyplot as plt


depok_obj = foi('Depok',crs=3857,zoom_level=17)

depok_school = depok_obj.area_of_interest({'amenity':'school'})