import sys
from collections import deque

# define graph class to store Wrestlers as vertices and rivalries as edges
class Graph:
    
    vertices = {}                       # store 
    isPossible = True
    startVertex = None
    babyfacesString = 'Babyfaces: '
    heelsString = 'Heels: '
    size = 0

    # add a new wrestler into the graph
    def addVertex(self, vertex):

        # verify the vertex is valid and does not already exist in the graph
        if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
            self.vertices[vertex.name] = vertex
            if self.size == 0:                  # this is the first node in the graph
                self.startVertex = vertex       # initialize starting point
                self.size = 1                   # initialize size of the graph
            return True
        else:
            return False

    # add a new rivalry, given two nodes
    def addEdge(self, u, v):

        # verify that both nodes exist in the graph
        if u in self.vertices and v in self.vertices:

            # iterate over every key-value pair in vertices
            for key, value in self.vertices.items():
                if key == v:
                    value.addNeighbor(u)
                if key == u:
                    value.addNeighbor(v)
            return True
        else:
            return False
    
    # print wrestlers on the babyface team
    def print_babyfaces(self):
        for wrestler in self.vertices:
            if self.vertices[wrestler].team == 'babyface':
                self.babyfacesString += (self.vertices[wrestler].name + ' ')
        print(self.babyfacesString)

    # print wrestlers on the heels team
    def print_heels(self):
        for wrestler in self.vertices:
            if self.vertices[wrestler].team == 'heel':
                self.heelsString += (self.vertices[wrestler].name + ' ')
        print(self.heelsString)

    # implement BFS to search if all wrestlers can be matched up as rivals
    def bfs(self, startVertex, visited):
        queue = deque()          # initiate queue
        
        startVertex.distance = 0
        visited.append(startVertex)
        startVertex.team = 'babyface'

        for adjNode in startVertex.neighbors:
            self.vertices[adjNode].distance = 1
            self.vertices[adjNode].team = 'heel'
            queue.append(adjNode)

        while len(queue) > 0:
            u = queue.popleft()
            node_u = self.vertices[u]
            visited.append(u)

            for v in node_u.neighbors:
                node_v = self.vertices[v]
                if v not in visited:
                    queue.append(v)

                    if node_v.distance > node_u.distance + 1:
                        node_v.distance = node_u.distance + 1
                    
                    if node_v.distance % 2 == 0:
                        node_v.team = 'babyface'
                    else:
                        node_v.team = 'heel'
                    
                    if node_v.team == node_u.team:
                        self.isPossible = False 


class Vertex:
    def __init__(self, n):
        self.name = n
        self.neighbors = list()
        self.distance = 1000
        self.team = 'none'

    def addNeighbor(self, v):
        if v not in self.neighbors:
            self.neighbors.append(v)
            self.neighbors.sort()


def main():

    # open file to read in data
    with open('wrestler1.txt') as f:
        g = Graph()         # initialize graph
        r = []              # initialize empty list to store rivalries

        lines = f.read().splitlines()

        # for each wrestler, create a vertex in the graph
        numWrestlers = int(lines[0])
        for i in range(1, numWrestlers + 1):
            g.addVertex(Vertex(lines[i]))

        # for each rivalry, create an edge between the two wrestlers in the graph
        for i in range(numWrestlers + 3, len(lines)):
            rivals = lines[i].split()
            g.addEdge(rivals[0], rivals[1])
        
        # start BFS from 
        visited = []
        g.bfs(g.startVertex, visited)
        
        if g.isPossible:
            print("Yes")
            g.print_babyfaces()
            g.print_heels()
        else:
            print("No")
        


if __name__ == "__main__":
    main()