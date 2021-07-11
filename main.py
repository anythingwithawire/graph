import keyboard
import sys
from random import randint
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
import time
import copy


def elog(msg):
    print("elog=>",msg)


class Nodes:
    def __init__(self):
        self.nodes = {}
        self.nodeTypes = {}
        self.nodeTypes['type'] = {}
        self.nodeTypes['type'] = {'type': 'terminal1', 'lineType': 'solid', 'lineColor': 'black', 'fillColor': 'none',
                                  'typeMemberOf': ['terminals', 'twoSided'], 'typeChildOf': 'root',
                                  'typeFosterOf': 'root', 'width': 100, 'height': 20, 'ports': {
                '001.1': {'pos': 1, 'side': 'left', 'type': 'square', 'size': 20, 'lx': 10, 'ly': 10, 'termNum': '01'},
                '001.2': {'pos': 1, 'side': 'right', 'type': 'square', 'size': 20, 'lx': 90, 'ly': 10, 'termNum': '01'}}}

        print(self.nodeTypes)

    def duplicateType(self, existing, new):
        self.nodeTypes[new] = {}
        self.nodeTypes[new] = {'type': {'type': new}}
        #self.nodeTypes[new]['type'][existing].copy()
        print("New Type", new, self.nodeTypes[new])

    def addNodeType(self, label, x, y, w, h, childOf):
        self.nodeTypes[label] = {}
        self.nodeTypes[label]['label'] = label
        self.nodeTypes[label]['width'] = w
        self.nodeTypes[label]['height'] = h
        self.nodeTypes[label]['x'] = x
        self.nodeTypes[label]['y'] = y
        self.nodeTypes[label]['childOf'] = childOf

#    nodes.addPort('terminal1', 2, '02', 100, 20, 'square', 'mid', 'left', 20)
    def addPortToType(self, label, portNum, termNum, port, lx, ly, shape, pos, side, size):
        if shape not in ['square', 'circle']:
            elog("shape not found, default to circle")
            shape = 'circle'
        if side not in ['left', 'right', 'mid']:
            elog("side not found, default to left")
            side = 'left'
        self.nodeTypes['type']['ports'][port] = {'pos': pos, 'side': side, 'type':'square', 'size': size, 'lx': lx, 'ly': ly , 'portNum': portNum, 'termNum': termNum }
        while ly > self.nodeTypes['type']['height']:
            self.nodeTypes['type']['height'] = self.nodeTypes['type']['height']+self.nodeTypes['type']['ports'][port]['size']



    def addNode(self, type, label, x, y, locChildOf):
        self.nodes[label] = {}
        self.nodes[label]['type'] = type
        self.nodes[label] = copy.deepcopy(self.nodeTypes['type'])
        # (self.nodes[str(label)])['type']['label'] = type
        self.nodes[label]['x'] = x
        self.nodes[label]['y'] = y
        self.nodes[label]['locChildOf'] = locChildOf

    def drawNode(self, tag, canvas):
        font = QtGui.QFont()
        font.setFamily('Calibri')
        font.setBold(False)
        font.setPointSize(6)
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor('blue'))
        pen.setWidth(3)
        canvas.setPen(pen)
        canvas.drawRoundedRect(self.nodes[tag]['x'], self.nodes[tag]['y'], self.nodes[tag]['width'],
                               self.nodes[tag]['height'], 20, 20, Qt.RelativeSize)
        canvas.drawText(self.nodes[tag]['x'], self.nodes[tag]['y'] - 20 + 2,
                        self.nodes[tag]['width'], 10, Qt.AlignHCenter | Qt.AlignVCenter, tag)
        font = QtGui.QFont()
        font.setFamily('Calibri')
        font.setBold(True)
        font.setPointSize(3)
        pen.setColor(QtGui.QColor('green'))
        pen.setWidth(1)
        canvas.setPen(pen)
        canvas.setFont(font)
        #canvas.drawText(self.nodes[tag]['x'], self.nodes[tag]['y'], self.nodes[tag]['width'], self.nodes[tag]['height'],
                        #Qt.AlignHCenter | Qt.AlignVCenter, tag)
        font.setPointSize(8)
        pen.setColor(QtGui.QColor('black'))
        pen.setWidth(1)
        canvas.setPen(pen)
        canvas.setFont(font)
        for p in self.nodes[tag]['ports']:
            #print("In drawNode >>",p,  p['lx'], p['ly'])
            canvas.drawEllipse(self.nodes[tag]['x'] + self.nodes[tag]['ports'][p]['lx'] - 2, self.nodes[tag]['y'] + self.nodes[tag]['ports'][p]['ly'] - 2, 6, 6)
            swidth  = canvas.fontMetrics().width(self.nodes[tag]['ports'][p]['termNum'])
            sheight = canvas.fontMetrics().height()


            if self.nodeTypes['type']['ports'][p]['side']=='left':
                #canvas.drawText(self.nodes[tag]['x'] + 6 + self.nodes[tag]['ports'][p]['lx'] , self.nodes[tag]['y'] -6 + self.nodes[tag]['ports'][p]['ly'], swidth*2, sheight, Qt.AlignVCenter | Qt.AlignLeft, self.nodes[tag]['ports'][p]['termNum'])
                canvas.drawText(self.nodes[tag]['x'] + 6 + self.nodes[tag]['ports'][p]['lx'],
                                self.nodes[tag]['y'] - 6 + self.nodes[tag]['ports'][p]['ly'], swidth * 2, sheight,
                                Qt.AlignVCenter | Qt.AlignLeft, self.nodes[tag]['ports'][p]['termNum'])
            if self.nodeTypes['type']['ports'][p]['side'] == 'right':
                canvas.drawText(self.nodes[tag]['x'] - 6 + self.nodes[tag]['ports'][p]['lx'] - swidth, self.nodes[tag]['y'] - 6+ self.nodes[tag]['ports'][p]['ly'], swidth, sheight, Qt.AlignVCenter | Qt.AlignRight,self.nodes[tag]['ports'][p]['termNum'])
                #canvas.drawText(self.nodes[tag]['x'] - 6 + self.nodes[tag]['ports'][p]['lx'] - swidth, self.nodes[tag]['y'] - 6+ self.nodes[tag]['ports'][p]['ly'], swidth, sheight, Qt.AlignVCenter | Qt.AlignRight,self.nodes[tag]['ports'][p]['termNum'])
        return(canvas)

    def drawAllNodes(self, canvas):
        for n in self.nodes:
            print("NNN>>>", n)
            canvas = self.drawNode(n, canvas)
            for p in self.nodes[n]['ports']:
                print("PPP>>>",self.nodes[n]['ports'][p]['lx'],self.nodes[n]['ports'][p]['ly'])

            print(self.nodes[n]['ports'])
        return(canvas)

class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent,
    it will appear as a free-floating window.
    """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0, 100))
        layout.addWidget(self.label)
        self.button1 = QPushButton("Push for Zoom In")
        self.button1.setFixedSize(100, 20)
        self.button1.clicked.connect(lambda checked: self.zoomIn_window())
        layout.addWidget(self.button1)

        self.button2 = QPushButton("Push for Zoom Out")
        self.button2.setFixedSize(100, 20)
        self.button2.clicked.connect(lambda checked: self.zoomOut_window())
        layout.addWidget(self.button2)
        self.setLayout(layout)

    def zoomIn_window(window):
        MainWindow.self.painter.scale(1.5, 1.5)
        MainWindow.canvas.scaledToWidth(500)
        MainWindow.nodes.drawAllNodes(MainWindow.painter)
        MainWindow.painter.end()

    def zoomOut_window(window):
        MainWindow.painter.scale(0.3, 0.3)
        MainWindow.canvas.scaledToWidth(500)
        MainWindow.nodes.drawAllNodes(MainWindow.painter)
        MainWindow.painter.end()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window1 = AnotherWindow()
        self.window2 = AnotherWindow()

        self.setMinimumSize(QSize(3550, 2100))
        self.window1.setMinimumSize(QSize(600, 2000))
        self.window2.setMinimumSize(QSize(600, 2000))



        self.nodes = Nodes()

        self.nodes.duplicateType('terminal1', 'terminals25')

        print("before>>", self.nodes.nodeTypes['type'])

        self.nodes.addNode('terminal1', 'LSL-1002', 300, 300, 'root')
        self.nodes.addNode('terminal1', 'LSH-1002', 500, 300, 'root')
        self.nodes.addNode('terminal1', 'LSA-1002', 800, 300, 'root')
        self.nodes.addPortToType('terminal1', 2, '02', '002.1', 90, 30, 'square', 'mid', 'right', 20)
        self.nodes.addPortToType('terminal1', 2, '02', '002.2', 10, 30, 'square', 'mid', 'left', 20)
        print("after>>", self.nodes.nodeTypes['type'])

        self.nodes.addNode('terminal1', 'LSB-1002', 900, 100, 'root')
        self.nodes.addNode('terminal1', 'LSC-1002', 1100, 100, 'root')
        self.nodes.addPortToType('terminal1', 3, '03', '003.1', 90, 50, 'square', 'mid', 'right', 20)
        self.nodes.addPortToType('terminal1', 3, '03', '003.2', 10, 50, 'square', 'mid', 'left', 20)
        self.nodes.addPortToType('terminal1', 4, '04', '004.1', 90, 70, 'square', 'mid', 'right', 20)
        self.nodes.addPortToType('terminal1', 4, '04', '004.2', 10, 70, 'square', 'mid', 'left', 20)
        self.nodes.addPortToType('terminal1', 5, '05', '005.1', 90, 90, 'square', 'mid', 'right', 20)
        self.nodes.addPortToType('terminal1', 5, '05', '005.2', 10, 90, 'square', 'mid', 'left', 20)
        self.nodes.addPortToType('terminal1', 6, '06', '006.1', 90, 110, 'square', 'mid', 'right', 20)
        self.nodes.addPortToType('terminal1', 6, '06', '006.2', 10, 110, 'square', 'mid', 'left', 20)
        self.nodes.addPortToType('terminal1', 7, '07', '007.1', 90, 130, 'square', 'mid', 'right', 20)
        self.nodes.addPortToType('terminal1', 7, '07', '007.2', 10, 130, 'square', 'mid', 'left', 20)
        self.nodes.addNode('terminal1', 'LSD-1002', 200, 500, 'root')
        self.nodes.addNode('terminal1', 'ASD-1002', 300, 900, 'root')
        self.nodes.addNode('terminal1', 'BSD-1002', 400, 500, 'root')
        self.nodes.addNode('terminal1', 'CSD-1002', 500, 900, 'root')
        self.nodes.addNode('terminal1', 'DSD-1002', 600, 500, 'root')
        self.nodes.addNode('terminal1', 'EED-1002', 700, 900, 'root')
        self.nodes.addNode('terminal1', 'ELD-1002', 800, 500, 'root')
        self.nodes.addNode('terminal1', 'FSD-1002', 900, 900, 'root')
        self.nodes.addNode('terminal1', 'GSD-1002', 1000, 500, 'root')
        self.nodes.addNode('terminal1', 'HSD-1002', 1100, 900, 'root')
        self.nodes.addNode('terminal1', 'ISD-1002', 1200, 500, 'root')
        self.nodes.addNode('terminal1', 'JLSD-1002', 1300, 900, 'root')
        print(self.nodes.nodes['LSL-1002'])

        l = QVBoxLayout()

        label = QtWidgets.QLabel()
        self.canvas = QtGui.QPixmap(3500, 2100)
        self.canvas.fill(Qt.darkGray)
        label.setPixmap(self.canvas)
        # setCentralWidget(self.label)
        l.addWidget(label)

        self.painter = QtGui.QPainter(label.pixmap())


        # nodes.drawNode('LSL-1002', painter)
        # nodes.drawNode('LSH-1002', painter)
        self.painter.scale(1.7,1.7)
        #painter = nodes.drawAllNodes(painter)


        self.painter = self.nodes.drawAllNodes(self.painter)
       # painter.end()
        #painter.scale(0.5, 0.5)
        self.canvas.scaledToWidth(500)
        self.painter = self.nodes.drawAllNodes(self.painter)

        self.show()

        self.painter.end()




        button1 = QPushButton("Push for Window 1")
        button1.setFixedSize(100, 20)
        button1.clicked.connect(lambda checked: self.toggle_window(self.window1, self.canvas, self.painter))
        l.addWidget(button1)

        button2 = QPushButton("Push for Window 2")
        button2.setFixedSize(100, 20)
        button2.clicked.connect(lambda checked: self.toggle_window(self.window2, self.canvas, self.painter))
        l.addWidget(button2)


        w = QWidget()
        w.setLayout(l)
        self.setCentralWidget(w)




    def toggle_window(self, window, canvas, painter):

        if window.isVisible():
            self.mygeo = window.saveGeometry()

            #self.toggle_window(self.window2)
            window.hide()
        else:
            window.show()
            l = QVBoxLayout()
            label = QtWidgets.QLabel()
            canvas = QtGui.QPixmap(500,500)
            canvas.fill(Qt.darkGray)
            label.setPixmap(canvas)
            # setCentralWidget(self.label)
            l.addWidget(label)

            w = QWidget()
            w.setLayout(l)
            #window.setCentralWidget(w)
            w.show()
            window.show()




app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()

'''
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(2400, 1300)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        l=[]
        n={}
        n['dim'] = [100, 100, 120, 150]
        n['labels'] = ['PSH-1002','Field', 'BMS-001']
        n['left'] = [[1,1,'+ve'],[2,1,'com'],[3,1,'-ve'],[4,1,'Start'],[5,1,'Stop'],[6,1,'E-Stop']]
        n['right'] = [[1, 1, '+ve'], [2, 1, 'com'], [3, 1, '-ve'], [4, 1, 'Start'], [5, 1, 'Stop'],[6, 1, 'E-Stop']]
        l.append(copy.deepcopy(n))
        k['PSH-0812'] = n
        n={}
        n['dim'] = [500, 100, 50, 150]
        n['labels'] = ['PSL-1002','Field', 'BMS-001']
        n['mid'] = [[1,1,'+ve'],[2,1,'com'],[3,1,'-ve'],[4,1,'Start'],[5,1,'Stop'],[6,1,'E-Stop']]
        l.append(copy.deepcopy(n))
        self.draw_node(l)
        k['PSL-1002'] = n
        
        print(k)

    def draw_node(self, nodes):

        portHeight = 15;
        portWidth = 15

        painter = QtGui.QPainter(self.label.pixmap())
        font = QtGui.QFont()
        font.setFamily('Calibri')
        font.setBold(False)
        font.setPointSize(6)
        painter.setFont(font)
        pen = QtGui.QPen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor('green'))

        pen = QtGui.QPen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor("#376F9F"))
        painter.setPen(pen)
        for n in nodes:
            #painter.drawRoundedRect(200, 150, 50, 200, 5, 5, Qt.RelativeSize)
            x = n['dim'][0]
            y = n['dim'][1]
            w = n['dim'][2]
            h = n['dim'][3]
            #painter.drawRoundedRect(x, y,w, h, 5, 5, Qt.RelativeSize)

            if 'left' in n:
                for p in n['left']:
                    painter.drawRoundedRect(x, y+(p[0]*portHeight), portWidth, portHeight, 5, 5, Qt.RelativeSize)
                    painter.drawText(x + int(portWidth*1.2), y + p[0]*portHeight,portWidth*2, portHeight, Qt.AlignHCenter, p[2])

            if 'right' in n:
                for p in n['right']:
                    painter.drawRoundedRect(x+w-portWidth, y + (p[0] * portHeight), portWidth, portHeight, 5, 5, Qt.RelativeSize)
                    painter.drawText(x + w - int(portWidth*3.6), y + p[0]*portHeight, portWidth*2, portHeight, Qt.AlignHCenter, p[2])

            if 'mid' in n:
                for p in n['mid']:
                    painter.drawRoundedRect(x, y+(p[0]*portHeight),w, portHeight, 5, 5, Qt.RelativeSize)
                    painter.drawText(x, y + p[0]*portHeight, w, portHeight, Qt.AlignHCenter, p[2])

            if 'labels' in n:
                for p in n['labels']:
                    #painter.drawRoundedRect(x, y+(p[0]*portHeight), portWidth, portHeight, 5, 5, Qt.RelativeSize)
                    painter.drawText(x + int(w/2), y + h * portHeight, w , portHeight, Qt.TextWordWrap + Qt.AlignHCenter, p[2])


            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawRoundedRect(x, y, w, h, 5, 5, Qt.RelativeSize)


        painter.end()
'''

'''
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
'''
