import networkx as nx
from queue import PriorityQueue
import numpy as np

# Implement the A* algorithm
def risk_a_star(graph, start, goal, arg_column):
    # Define the custom g-score function
    def custom_g_score(current, neighbor, graph):
        risk_current = graph.nodes[current][arg_column]
        risk_neigh = graph.nodes[neighbor][arg_column]
        pos_current = graph.nodes[current]['position']
        pos_neigh = graph.nodes[neighbor]['position']

        distance_euclid = distance_euclid = np.linalg.norm(pos_current - pos_neigh) 
        score_g = ((risk_current+risk_neigh)/2) * distance_euclid
        return score_g

    # Define the custom h-score function
    def custom_h_score(current, goal, graph):
        risk_current = graph.nodes[current][arg_column]
        risk_goal = graph.nodes[goal][arg_column]
        pos_current = graph.nodes[current]['position']
        pos_goal = graph.nodes[goal]['position']

        distance_euclid = distance_euclid = np.linalg.norm(pos_current - pos_goal) 
        score_h = ((risk_current+risk_goal)/2) * distance_euclid 

        return score_h
    
    open_set = PriorityQueue()
    open_set.put((0, start))

    g_score = {start: 0}
    h_score = {start: custom_h_score(start,goal, graph)}
    f_score = {start: h_score[start]}
    came_from = {}
    



    while not open_set.empty():
        _, current = open_set.get()

        if current == goal:
            # Reached the goal node, construct and return the path
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor in graph.neighbors(current):
            g = g_score[current] + custom_g_score(current, neighbor, graph)
            h = custom_h_score(neighbor, goal, graph)
            f = g + h

            if neighbor not in g_score or g < g_score[neighbor]:
                g_score[neighbor] = g
                h_score[neighbor] = h
                f_score[neighbor] = f
                open_set.put((f, neighbor))
                came_from[neighbor] = current

    # No path found
    return None
