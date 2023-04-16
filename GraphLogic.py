# Определяем класс Node
class Node:

    # Конструктор класса Node
    def __init__(self, name):
        # Поля класса Node
        self.links = [] # список связанных узлов (типа Link)
        self.visited = False # флаг, определяющий, посещен ли узел в процессе обхода графа
        self.name = name # имя узла
        self.x = None # координата x
        self.y = None # координата y

    # Переопределение метода __repr__ для удобства отладки
    def __repr__(self) -> str:
        return f"<name = {self.name}, visited = {self.visited}"
    
    # Переопределение метода __str__ для удобного вывода информации о узле
    def __str__(self) -> str:
        return f"<name = {self.name}, visited = {self.visited}, x = {self.x}, y = {self.y} ,links = {self.links}>"
    
    # Переопределение метода __add__ для удобного сложения строк
    def __add__(self, other):
        return str(self) + other
    
    # Переопределение метода __radd__ для удобного сложения строк
    def __radd__(self, other):
        return other + str(self)
    
    # Метод класса Node, который помечает узел как посещенный
    def visit(self):
        self.visited = True

    # Методы класса Node для установки и получения координат x и y
    def setX(self, cordX: int):
        self.x = cordX

    def setY(self, cordY: int):
        self.y = cordY

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    

# Определяем класс Link
class Link:

    # Конструктор класса Link
    def __init__(self, origin, destination, ):
        # Поля класса Link
        self.origin = origin # исходный узел (типа Node)
        self.destination = destination # узел назначения (типа Node)
        self.visited = False # флаг, определяющий, посещена ли связь в процессе обхода графа

    # Переопределение метода __repr__ для удобства отладки
    def __repr__(self) -> str:
        return f"visited = {self.visited}, origin = {self.origin.name}, destination = {self.destination.name}"

    # Метод класса Link, который помечает связь как посещенную
    def visit(self):
        self.visited = True

    # Метод класса Link, который возвращает узел назначения в зависимости от переданного узла-источника
    def getDest(self, origin):
        if origin is self.origin:
            return self.destination
        else:
            return self.origin


# Определяем класс Graph
class Graph:

    def __init__(self):
        self.nodes = []   # создание списка вершин графа
        self.inc = 0      # переменная для назначения имени новой вершине (увеличивается на 1 при добавлении новой вершины)
        self.visitList = []   # список посещенных вершин

    def __repr__(self) -> str:   # метод возвращающий строковое представление графа (для удобства вывода)
        string = ""
        for node in self.nodes:
            string += str(node) + "\n"
        return string
    
    def visit(self, node):   # метод помечает вершину как посещенную и добавляет ее в список посещенных вершин
        self.visitList.append(node)
        node.visit()

    def add(self):   # метод добавляет новую вершину в граф и возвращает ее
        nodeObj = Node(self.inc)
        self.__add(nodeObj)
        self.inc += 1
        return nodeObj

    def __add(self, node):   # метод добавляет вершину в список вершин графа
        self.nodes.append(node)

    def createLink(self, source, destination):   # метод создает ребро между двумя вершинами
        source: Node = self.nodes[source]   # получаем вершину-источник по ее индексу в списке вершин
        destination = self.nodes[destination]   # получаем вершину-назначение по ее индексу в списке вершин
        link = Link(source,destination)   # создаем новое ребро между вершинами
        source.links.append(link)   # добавляем ребро в список ребер вершины-источника
        return link   # возвращаем созданное ребро

    def deepSearch(self):   # метод запускает поиск в глубину начиная с первой вершины графа
        self.__deepSearch(self.nodes[0])

    def deepSearchGen(self, node:Node):   # метод генератор, который осуществляет поиск в глубину по шагам (возвращает текущую вершину, которую обрабатывает и все ее непосещенные соседние вершины)
        if node in self.visitList:   # если вершина уже посещена, возвращаем ее
            yield node
        self.visit(node)   # помечаем вершину как посещенную
        yield node   # возвращаем текущую вершину
        for nod in node.links:   # проходимся по всем ребрам вершины и обрабатываем непосещенные соседние вершины
            if nod.destination not in self.visitList:
                nod.visit()
                yield nod
                yield from self.deepSearchGen(nod.destination)

    def __deepSearch(self, node: Node):   # рекурсивный метод поиска в глубину (вызывает себя для всех непосещенных сосед
        if node in self.visitList:
            return
        self.visit(node)

        for nod in node.links:
            if nod.destination not in self.visitList:
                nod.visit()
                self.__deepSearch(nod.destination)

        # if len(node.links) != 0:
        #     self.__deepSearch(node.links[0])
        # return

    def deleteAll(self):
        self.inc = 0 
        self.nodes = []
        self.visitList = []


#тестирование
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
    
    x = graph.deepSearchGen(graph.nodes[0])
    print(next(x))
    print("-----------")
    print(graph)
    print("-----------")
    print(next(x))
    print("-----------")
    print(graph)
    print("-----------")
    print(next(x))
    print("-----------")
    print(graph)
    print("-----------")
    print(next(x))
    print("-----------")
    print(graph)
    print("-----------")