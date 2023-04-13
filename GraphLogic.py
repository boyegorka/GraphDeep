class Node:

    def __init__(self, name):
        self.links = []
        self.visited = False
        self.name = name

    def __repr__(self) -> str:
        return f"<name = {self.name}, visited = {self.visited}"
    

    def __str__(self) -> str:
        return f"<name = {self.name}, visited = {self.visited}, links = {self.links}>"
        
    # def addLink(self, node):
    #     self.links.append(Node)

    def visit(self):
        self.visited = True


class Graph:

    def __init__(self):
        self.nodes = []
        self.inc = 0 
        self.visitList = []

    def __repr__(self) -> str:
        string = ""
        for node in self.nodes:
            string += str(node) + "\n"
        return string
    
    def visit(self, node):
        self.visitList.append(node)
        node.visit()
        print(node)

    def add(self):
        self.__add(Node(self.inc))
        self.inc += 1

    def __add(self, node):
        self.nodes.append(node)

    def createLink(self, source, destination):
        source: Node = self.nodes[source]
        destination = self.nodes[destination]
        source.links.append(destination)
        destination.links.append(source)

    def deepSearch(self):
        self.__deepSearch(self.nodes[0])


    def __deepSearch(self, node: Node):
        if node in self.visitList:
            return
        self.visit(node)

        for nod in node.links:
            if nod not in self.visitList:
                self.__deepSearch(nod)

        # if len(node.links) != 0:
        #     self.__deepSearch(node.links[0])
        # return


if __name__ == "__main__":
    graph = Graph()
    graph.add()
    graph.add()
    graph.add()
    graph.add()
    graph.add()
    graph.add()
    graph.add()

    graph.createLink(0,1)
    graph.createLink(0,2)
    graph.createLink(0,3)
    graph.createLink(1,2)
    graph.createLink(2,4)
    print(graph.nodes)
    print(graph)
    graph.deepSearch()

