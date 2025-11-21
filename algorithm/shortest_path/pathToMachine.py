import heapdict
import csv
from munchi_maps_model import MunchiMaps_model
from haversine import haversine, Unit # used to calculate the distance between two longitudes and latitudes

class path_graph(object):
    def __init__(self, csv_file):
        self.path_data = csv_file
        self.graph = []
        self.loadGraph()
    def loadGraph():
        # CREATE DICT OF EDGES
        
    #def closestNode():
        # FIND THE NODE CLOSEST TO THE USER TO START THE PATH
    #def dijkstra():
        # FIND SHORTEST PATH ACROSS THE GRAPH CREATED

class node(object):
    def __init__(self, num, latitude, longitude):
        self.n = num
        self.lat = latitude
        self.long = longitude