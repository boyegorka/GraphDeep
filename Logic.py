import sys  # импортируем sys для работы с системными параметрами и функциями
import GraphLogic  # импортируем наш модуль GraphLogic
import math  # импортируем модуль math для работы с математическими функциями
import exception  # импортируем наш модуль exception
from PyQt6.QtWidgets import *  # импортируем все виджеты из PyQt6.QtWidgets
from Design import Ui_MainWindow  # импортируем Ui_MainWindow из нашего модуля Design
from PyQt6 import *  # импортируем все модули из PyQt6
from math import *  # импортируем все из модуля math
from PyQt6.QtCore import QRect, Qt  # импортируем QRect и Qt из PyQt6.QtCore

nodeNum = 0  # количество узлов
pathNum = 0  # количество путей
pixmapWidth = 621  # ширина изображения
pixmapHeight = 530  # высота изображения

class GUI:  # создаем класс GUI для нашего приложения

    def __init__(self) -> None:  # создаем конструктор класса GUI
        app = QApplication(sys.argv)  # создаем объект приложения QApplication
        MainWindow = QMainWindow()  # создаем объект главного окна приложения
        self.ui = Ui_MainWindow()  # создаем объект пользовательского интерфейса Ui_MainWindow
        self.ui.setupUi(MainWindow)  # настраиваем пользовательский интерфейс Ui_MainWindow
        MainWindow.show()  # отображаем главное окно приложения
        self.graph = GraphLogic.Graph()  # создаем объект класса Graph из модуля GraphLogic
        self.scene = QGraphicsScene()  # создаем объект QGraphicsScene
        self.pixmap = QtGui.QPixmap(pixmapWidth, pixmapHeight)  # создаем объект QPixmap
        self.painter = QtGui.QPainter()  # создаем объект QPainter
        self.flipflop = True  # флаг переключения
        self.firstOn = True  # флаг первого включения

        # подключаем кнопки к слотам
        self.ui.continueButton.clicked.connect(self.setPathsAndNodes)  
        self.ui.createButton.clicked.connect(self.callAll)
        self.ui.clearButton.clicked.connect(self.clearAll)
        self.ui.nextButton.clicked.connect(self.updateState)

        sys.exit(app.exec())  # запускаем приложение

    def callAll(self):
        # Очищение поля графики
        self.clearGraphicView()
        # Эта функция вызывает другие функции, необходимые для реализации основной функциональности приложения. 
        # Она также обрабатывает исключения, которые могут возникнуть в результате некорректного ввода пользователем.
        self.ui.nextButton.setEnabled(True) # Активирует кнопку "Далее" на главном окне приложения.
        self.createNode() # Создает вершины в графическом интерфейсе.


        try:
            self.createPaths() # Создает связи между вершинами графа.
            self.gen = self.graph.deepSearchGen(self.graph.nodes[0]) # Инициализирует генератор глубокого поиска для графа.
        except exception.incorectPathWay: # Если возникает исключение, связанное с некорректными путями, выводится сообщение об ошибке.
            self.message("Вы вышли за пределы количества нодов или не указали верных путей", QMessageBox.Icon.Information)
            self.clearGraphicView()

        # self.createPaths() # Создает связи между вершинами графа.
        # self.gen = self.graph.deepSearchGen(self.graph.nodes[0]) # Инициализирует генератор глубокого поиска для графа.
        # self.message("Вы вышли за пределы количества нодов или не указали верных путей", QMessageBox.Icon.Information)
        # self.clearGraphicView()


    def message(self, message: str, icon: QMessageBox): # Функция для создания окна с сообщением об ошибке.
        error_dialog = QMessageBox()
        error_dialog.setIcon(icon) # Устанавливает иконку для окна с сообщением об ошибке.
        error_dialog.setWindowTitle("Оповещение") # Устанавливает заголовок для окна с сообщением об ошибке.
        error_dialog.setText(message) # Устанавливает текст для окна с сообщением об ошибке.
        error_dialog.exec() # Отображает окно с сообщением об ошибке.

    def setPathsAndNodes(self):
        # получаем значения количества узлов и путей из элементов интерфейса
        self.nodeNum = int(self.ui.nodeSpinBox.text())
        self.pathNum = int(self.ui.pathSpinBox.text())
        # устанавливаем количество строк в таблице путей и задаем заголовки
        self.ui.tableView.setRowCount(self.pathNum)
        self.ui.tableView.setColumnCount(2)
        self.ui.tableView.setHorizontalHeaderLabels(["Откуда", "Куда"])
        
        # выводим сообщение о создании путей графа
        if self.firstOn:
            self.message("При создании путей графа помните:\n Граф создаётся с нулевой ноды, то есть вам всегда нужно проводить пути начиная с нуля", QMessageBox.Icon.Information)
            self.firstOn = False

        # разблокируем кнопку создания графа
        self.ui.createButton.setEnabled(True)


    def drawNode(self, start, nodeName, visitState=False):
        painter = QtGui.QPainter(self.pixmap) # создаем экземпляр класса QPainter для рисования элементов на графической сцене
        text = str(nodeName)
        center_x, center_y = start[0], start[1]
        circle_radius = 10 
        if visitState == True:
            color = QtGui.QColor("#32CD32") # задаем цвет для посещенного узла
        else:
            color = QtGui.QColor("#FF0000") # задаем цвет для не посещенного узла
        painter.setBrush(QtGui.QColor("white")) # устанавливаем цвет заливки для узла
        painter.drawEllipse(center_x - circle_radius, center_y - circle_radius, 2 * circle_radius, 2 * circle_radius) # рисуем круговую рамку для узла
        painter.setPen(QtGui.QPen(color, 2)) # задаем цвет для круговой рамки
        painter.drawEllipse(center_x - circle_radius, center_y - circle_radius, 2 * circle_radius, 2 * circle_radius) # рисуем круговую рамку с цветом на узле
        text_rect = painter.boundingRect(QRect(center_x - circle_radius, center_y - circle_radius, 2 * circle_radius, 2 * circle_radius), Qt.AlignmentFlag.AlignCenter, text) # задаем область вывода текста на узле
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, text) # рисуем текст на узле
        self.scene.addPixmap(self.pixmap) # добавляем рисунок в графическую сцену
        self.ui.graphicsView.setScene(self.scene) # выводим графическую сцену в интерфейс


    def drawPath(self, start, destination, visitState=False):
        # Инициализация объекта для рисования
        painter = QtGui.QPainter(self.pixmap)
        # Задание цвета линии в зависимости от флага состояния пути
        if visitState == True:
            color = QtGui.QColor("#32CD32") # Зеленый цвет для посещенного пути
        else:
            color = QtGui.QColor("#FF0000") # Красный цвет для не посещенного пути
        painter.setPen(QtGui.QPen(color, 2)) # Задание цвета и толщины пера для рисования линии
        painter.drawLine(start[0], start[1], destination[0], destination[1]) # Начало рисования линии от стартовой точки до конечной точки
        self.scene.addPixmap(self.pixmap) # Добавление изображения на графическую сцену
        self.ui.graphicsView.setScene(self.scene) # Установка графической сцены в графический виджет

    def createNode(self):
        self.graph.deleteAll() # Удаление всех узлов из графа
        centerX, centerY = pixmapWidth // 2, pixmapHeight // 2 # Определение координат центра изображения
        radius = 150 # Определение радиуса окружности на которой будут расположены узлы

        # Цикл для создания заданного количества узлов
        for i in range(self.nodeNum):
            # Расчет угла на окружности для текущего узла
            angle = 2 * math.pi * i / self.nodeNum
            # Расчет координат стартовой точки для текущего узла на окружности
            startX = int(centerX + radius * cos(angle))
            startY = int(centerY + radius * sin(angle))
            # Добавление узла в граф и задание ему координат
            n = self.graph.add()
            n.setX(startX)
            n.setY(startY)
            # Отрисовка узла на графической сцене
            self.drawNode((startX, startY), n.name)

    def createPaths(self):
        self.links = [] # Создание списка связей
        counter = 0 # Счётчик путей
        # Цикл while для создания путей
        while counter < self.pathNum:
            try:
                # Получение начальной и конечной вершин пути из таблицы
                self.fromNode = self.ui.tableView.item(counter,0).text()
                self.toNode = self.ui.tableView.item(counter,1).text()
            except AttributeError:
                # Если произошла ошибка получения вершин из таблицы, выброс исключения
                raise exception.incorectPathWay

            # Проверка, что номера начальной и конечной вершин попадают в диапазон от 0 до (количество вершин - 1)
            print("fromNode", type(self.fromNode), "toNode", type(self.toNode), "NodeNum", range(0,self.nodeNum-1))
            if int(self.fromNode) in range(0, int(self.nodeNum)) and int(self.toNode) in range(0, int(self.nodeNum)):
                # Если проверка пройдена успешно, добавление связи в список связей
                self.links.append((int(self.fromNode), int(self.toNode)))
                # Увеличение счётчика 
            else:
                # Если проверка не пройдена, выброс исключения
                raise exception.incorectPathWay

            # self.links.append((int(fromNode), int(toNode)))
            
            counter += 1
            
        # Цикл for для создания связей
        for link in self.links:
            # Создание связи между начальной и конечной вершинами
            lin = self.graph.createLink(link[0], link[1])
            # Получение координат начала и конца связи
            startX = lin.origin.getX()
            startY = lin.origin.getY()
            destX = lin.destination.getX()
            destY = lin.destination.getY()
            # Отрисовка связи
            self.drawPath((startX,startY),(destX, destY))

    def updateState(self):
        try: 
            if self.flipflop:
                node = next(self.gen) # Получение следующей вершины
                print(node) # Вывод в консоль информации о вершине
                state = node.visited # Получение состояния посещения вершины
                self.drawNode((node.getX(), node.getY()),node.name, visitState=state) # Отрисовка вершины
                self.flipflop = False # Переключение флага
            else:
                link = next(self.gen) # Получение следующей связи
                print(link) # Вывод в консоль информации о связи
                self.drawPath((link.origin.getX(), link.origin.getY()), (link.destination.getX(), link.destination.getY()), visitState = link.visited) # Отрисовка связи
                self.flipflop = True # Переключение флага
        except StopIteration:
            # Если достигнут конец генератора, то ничего не делать
            pass

    def clearAll(self):
        # Отключить кнопки "Следующий шаг" и "Создать граф"
        self.ui.nextButton.setEnabled(False)
        self.ui.createButton.setEnabled(False)
        # Установить значения счетчиков узлов и путей в 0
        self.ui.nodeSpinBox.setValue(0)
        self.ui.pathSpinBox.setValue(0)
        # Удалить все строки и столбцы из таблицы узлов и путей
        self.ui.tableView.setRowCount(0)
        self.ui.tableView.setColumnCount(0)
        # Удалить все узлы и пути из графа
        self.graph.deleteAll()
        # Очистить графическое представление графа
        self.clearGraphicView()
        # Создать новый пустой граф
        self.graph = GraphLogic.Graph()
        # Установить флаг flipflop в True
        self.flipflop = True

    def clearGraphicView(self):
        self.pixmap.fill(QtGui.QColor("#302F2E")) # Заполнить pixmap черным цветом
        self.scene.addPixmap(self.pixmap) # Добавить pixmap на сцену

if __name__ == "__main__" :
    GUI() # Запустить пользовательский интерфейс