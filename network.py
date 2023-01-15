import heapq
import sys # for use in djkiateirnstoeira's algorithm

# vertex
# possibly will have more stuff later, hence the class
class Building:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __lt__(self, other):
        return self.name < other.name

# undirected weighted edge
class Connection:
    def __init__(self, b1, b2, weight):
        self.b1 = b1
        self.b2 = b2
        self.weight = weight
    
    def __repr__(self):
        return self.b1+"-"+self.b2+":"+str(self.weight)

# graph
class BuildingNetwork:
    def __init__(self):
        self.buildings = []
        self.connections = []

    def set_buildings(self, bs):
        self.buildings = bs
    
    def set_connections(self, cs):
        self.connections = cs

    def get_building(self, name):
        for b in self.buildings:
            if b.name == name: return b

    def get_neighbours(self, building):
        nbs = []
        for c in self.connections:
            if c.b1 == building: nbs.append((c.b2, c.weight))
            elif c.b2 == building: nbs.append((c.b1, c.weight))
        return nbs

    # uses dijkstras. code adapted from max burstein (maxburstein.com)
    def find_shortest_path(self, b1, b2):
        distances = {} # {building: distance from b1 to building}
        bs = [] # heapqueue of buildings to check
        previous = {} # {building: previous building in shortest path}

        # initialize bus and distances
        for b in self.buildings:
            if b == b1:
                distances[b] = 0
                heapq.heappush(bs, [0,b])
            else:
                distances[b] = sys.maxsize
                heapq.heappush(bs, [sys.maxsize,b])
            previous[b] = None
        
        # fill distances
        while bs:
            closest = heapq.heappop(bs)[1]
            # found b2
            if closest == b2 and distances[closest] != sys.maxsize:
                path = [b2]
                while previous[closest]:
                    closest = previous[closest]
                    path.append(closest)
                path.reverse() # bad form, but I'm lazy
                return path
            # never found b2 (all remaining nodes are inaccessible)
            if distances[closest] == sys.maxsize:
                return None
            # otherwise
            nbs = self.get_neighbours(closest)
            for nb in nbs: # note that nb is in the form (building, weight)
                alt_dist = distances[closest] + nb[1]
                if alt_dist < distances[nb[0]]:
                    distances[nb[0]] = alt_dist
                    previous[nb[0]] = closest
                    # remake heap
                    for b in bs:
                        if b[1] == nb[0]:
                            b[0] = alt_dist
                            break
                    heapq.heapify(bs)