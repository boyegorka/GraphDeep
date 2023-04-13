from PyQt6.QtWidgets import *
from Design import Ui_MainWindow
from PyQt6 import uic, QtGui, QtWidgets
from random import randint
from numpy import array
from math import *
import sympy
import Design
import langdetect
import cld2
import numpy as np
import sys
import GraphLogic


import matplotlib.pyplot as plotlib


nodeNum = 0
pathNum = 0


class GUI:

    def __init__(self) -> None:
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)
        MainWindow.show()
        self.graph = GraphLogic.Graph()

        self.ui.continueButton.clicked.connect(self.setPathsAndNodes)
        self.ui.createButton.clicked.connect(self.callAll)
        self.ui.clearButton.clicked.connect(self.clearAll)

        sys.exit(app.exec())


    def setPathsAndNodes(self):
        self.nodeNum = int(self.ui.nodeSpinBox.text())
        self.pathNum = int(self.ui.pathSpinBox.text())

        self.ui.tableView.setRowCount(self.pathNum)
        self.ui.tableView.setColumnCount(2)
        self.ui.tableView.setHorizontalHeaderLabels(["Откуда", "Куда"])


    def getGraph(self):
        self.links = []
        counter = 0
        while counter < self.pathNum:

            fromNode = self.ui.tableView.item(counter,0).text()
            toNode = self.ui.tableView.item(counter,1).text()
            print(fromNode)
            print(toNode)
            #graph[fromNode] = toNode
            self.links.append((int(fromNode), int(toNode)))
            
            counter += 1
        
        print(self.links)

        for node in range(0, self.nodeNum):
            self.graph.add()
        
        for link in self.links:
            self.graph.createLink(link[0], link[1])

        print(self.graph)


    def alert(title, message): #Окно ошибок
        alert = QMessageBox()
        alert.setWindowTitle(title)
        alert.setText(message)
        alert.exec()

    def callAll(self):
        self.getGraph()

    def clearAll(self):
        self.ui.nodeSpinBox.setValue(0)
        self.ui.pathSpinBox.setValue(0)
        self.ui.tableView.setRowCount(0)
        self.ui.tableView.setColumnCount(0)


# # Алгоритм
# def dfs(graph, start, visited=None):
#     if visited is None:
#         visited = set()
#     visited.add(start)

#     print(start)

#     for next in graph[start] - visited:
#         dfs(graph, next, visited)
#     return visited


# graph = {'0': set(['1', '2']),
#          '1': set(['0', '3', '4']),
#          '2': set(['0']),
#          '3': set(['1']),
#          '4': set(['2', '3'])}



if __name__ == "__main__" :

    GUI()
