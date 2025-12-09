import csv
from heapdict import heapdict
from haversine import haversine, Unit


class Node:
    def __init__(self, num, latitude, longitude):
        self.id = int(num)
        self.lat = float(latitude)
        self.long = float(longitude)

    def coords(self):
        return (self.lat, self.long)


class PathGraph:
    def __init__(self, csv_file):
        self.csv_file = csv_file

        # id → Node object
        self.nodes = {}

        # adjacency list: id → {neighbor_id: distance}
        self.graph = {}

        self.loadGraph()

    def loadGraph(self):
        """
        loads nodes from CSV and builds adjacency list.
        CSV format:
            number, lat, long, connected
        connected can be:
            "2"
            "1.2"
            "1,2,3"
        """
        with open(self.csv_file, newline='') as f:
            reader = csv.DictReader(f)

            for row in reader:
                node_id = int(row["Number"])
                lat = float(row["Lat"])
                lon = float(row["Long"])

                # Create the Node
                self.nodes[node_id] = Node(node_id, lat, lon)
                self.graph[node_id] = {}

        # second pass: build edges
        with open(self.csv_file, newline='') as f:
            reader = csv.DictReader(f)

            for row in reader:
                node_id = int(row["Number"])
                connected = row["Connected"].strip()

                if not connected:
                    continue

                # split by comma and split "1.2" → ["1", "2"]
                raw_parts = connected.replace(".", ",").split(",")

                neighbors = []
                for p in raw_parts:
                    if p.strip().isdigit():
                        neighbors.append(int(p))

                # add edges
                for nb in neighbors:
                    if nb in self.nodes:
                        dist = haversine(
                            self.nodes[node_id].coords(),
                            self.nodes[nb].coords(),
                            unit=Unit.METERS
                        )
                        # undirected graph
                        self.graph[node_id][nb] = dist
                        self.graph[nb][node_id] = dist


    def closestNode(self, user_long, user_lat):
        # return the node ID that is geographically closest to the user
        min_dist = float("inf")
        closest = None

        for nid, node in self.nodes.items():
            d = haversine((user_lat, user_long), node.coords(), unit=Unit.METERS)
            if d < min_dist:
                min_dist = d
                closest = nid

        return closest


    def dijkstra(self, start_node):
        # return distance + previous maps starting from a given node
        dist = {nid: float("inf") for nid in self.nodes}
        prev = {nid: None for nid in self.nodes}

        dist[start_node] = 0

        pq = heapdict()
        pq[start_node] = 0

        while pq:
            current, cur_dist = pq.popitem()

            for neighbor, weight in self.graph[current].items():
                alt = cur_dist + weight
                if alt < dist[neighbor]:
                    dist[neighbor] = alt
                    prev[neighbor] = current
                    pq[neighbor] = alt

        return dist, prev

    def reconstruct_path(self, prev, end_node):
        # return list of nodes making up the path
        path = []
        curr = end_node
        while curr is not None:
            path.append(curr)
            curr = prev[curr]
        return path[::-1]
