import sys
from PyQt4 import QtGui, QtCore


class Test():
    def __init__(self, engine):
        self._engine = engine
        self._board = self._engine.getboard()
        print self._board.getwidth()
        print self._board.getheight()


class BoardRenderer(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.pen = QtGui.QPen(QtGui.QColor(0,0,0,0))
        self.pen.setWidth(3)
        self.brush = QtGui.QBrush(QtGui.QColor(255,255,255,20))

        self.char_001 = QtGui.QImage("./nibbles/gui/img/char_001.png")
        self.char_001active = QtGui.QImage("./nibbles/gui/img/char_001active.png")
        self.food = QtGui.QImage("./nibbles/gui/img/food.png")

        self.ziel1 = QtCore.QRect(165, 66, 30, 30)
        self.ziel2 = QtCore.QRect(264, 132, 30, 30)
        self.ziel3 = QtCore.QRect(297, 165, 30, 30)

        self.quelle = QtCore.QRect(0, 0,
            self.char_001.width(),
            self.char_001.height())


    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)

        #dimensions of a rectangle
        self.width = 33
        self.height = 33

        #range in rectangles
        for y in range(10):
            for x in range(16):
                painter.drawRect((self.width*x), (self.height*y), 30 ,30)


        painter.drawImage(self.ziel1, self.char_001, self.quelle)
        painter.drawImage(self.ziel2, self.char_001active, self.quelle)
        painter.drawImage(self.ziel3, self.food, self.quelle)



