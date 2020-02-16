import sys
from collections import deque

class Graph:
    
    vertices = {}
    isPossible = True
    babyfaces = 'Babyfaces: '
    heels = 'Heels: '
    startVertex = None
    size = 0

    def addVertex(self, vertex):
        if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
            self.vertices[vertex.name] = vertex
            if self.size == 0:
                self.startVertex = vertex
                self.size = 1
            return True
        else:
            return False

    def addEdge(self, u, v):
        if u in self.vertices and v in self.vertices:
            for key, value in self.vertices.items():
                if key == u:
                    value.addNeighbor(v)
                if key == v:
                    value.addNeighbor(u)
            return True
        else:
            return False
    
    def print_babyfaces(self):
        for wrestler in self.vertices:
            if self.vertices[wrestler].team == 'babyface':
                self.babyfaces = self.babyfaces + self.vertices[wrestler].name + ' '
        print(self.babyfaces)

    def print_heels(self):
        for wrestler in self.vertices:
            if self.vertices[wrestler].team == 'heel':
                self.heels = self.heels + self.vertices[wrestler].name + ' '
        print(self.heels)

    # try different BFS method
    def bfs(self, startVertex):
        queue = deque()          # initiate queue
        
        startVertex.distance = 0
        startVertex.color = 'grey'
        startVertex.team = 'babyface'

        for adjNode in startVertex.neighbors:
            self.vertices[adjNode].distance = 1
            self.vertices[adjNode].team = 'heel'
            queue.append(adjNode)

        while len(queue) > 0:
            u = queue.popleft()
            node_u = self.vertices[u]
            node_u.color = 'grey'

            for v in node_u.neighbors:
                node_v = self.vertices[v]
                if node_v.color == 'white':
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
        self.color = 'white'
        self.team = 'none'

    def addNeighbor(self, v):
        if v not in self.neighbors:
            self.neighbors.append(v)
            self.neighbors.sort()


def main():

    # open file to read in data
    with open('wrestler2.txt') as f:
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
        g.bfs(g.startVertex)
        
        if g.isPossible:
            print("Yes")
            g.print_babyfaces()
            g.print_heels()
        else:
            print("No")
        


if __name__ == "__main__":
    main()