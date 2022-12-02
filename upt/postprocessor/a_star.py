import numpy as np
import networkx as nx
from libpysal.weights import Queen
import warnings

from ..utils.geo_utils import GeoHandler

warnings.filterwarnings("ignore", category=DeprecationWarning) 
np.seterr(all=None)

def standar_heuristic(current_attr,neig_attr):                                 
    x1,y1 = current_attr['position']
    x2,y2 = neig_attr['position']
    return (((x2 - x1) ** 2 + (y2 - y1) ** 2))

class AStar:
    def __init__(self, gdf , arg_column, crs, custom_func=None):
        # Add error check for string
        self.crs = crs
        if isinstance(arg_column,str):
            self.arg_column = [arg_column]
        elif isinstance(arg_column,list):
            pass
        
        if(all(x in list(gdf.columns) for x in self.arg_column)):
            pass
        else:
            raise Exception("Warning argument column(agr_column) does not match with GeoPandas DataFrame column(gdf)")
        
        self.gdf = gdf
        self.custom_func = custom_func
        self.centroids = np.column_stack((gdf.to_crs(self.crs).centroid.x, gdf.to_crs(self.crs).centroid.y))
        
        self.contiguity = Queen.from_dataframe(gdf)
        self.graph = self.contiguity.to_networkx()
        
        self.node_positions = dict(zip(self.graph.nodes, self.centroids))
        nx.set_node_attributes(self.graph, self.node_positions,name='position')
        
        for column in self.arg_column:
            nx.set_node_attributes(self.graph,  gdf[column], name=column)
        nx.set_node_attributes(self.graph,  gdf.index, name='id')
    
    def create_line(self):
        self.point_line = []
        for node in (self.path_finder):
            self.point_line.append(self.graph.nodes[node]['position'])
        self.point_line = np.array(self.point_line)
        return (self.point_line)
    
    def heuristic_func_generator(self,current, neighbour):
        current_attr = self.graph.nodes[current]
        neighbour_attr = self.graph.nodes[neighbour]
        
        if self.custom_func == None:
            return (standar_heuristic(current_attr,neighbour_attr))
        else:
            return (self.custom_func(current_attr,neighbour_attr))
    
    def run_instance(self,start_node,end_node):
        gh = GeoHandler()
        self.start_node = gh.node_select(self.gdf,start_node)
        self.end_node = gh.node_select(self.gdf,end_node)
        self.path_finder = nx.astar_path(self.graph, (self.start_node), (self.end_node), heuristic=self.heuristic_func_generator)
        return(self.path_finder)