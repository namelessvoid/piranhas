import sys
from PyQt4 import QtGui, QtCore, uic
from logging import log
import datetime


class ServerGui(QtGui.QMainWindow):
    def __init__(self, engine):
        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi("./nibbles/gui/servergui.ui", self)

        for i in range(100):
            text = "Logger 08:08:2012 - INFO: Test logger" + str(i)
            self.ui.logger.append(text.rstrip())

        self._engine = engine
        self._engine.updatesignal.register(self.update)

        self.ui.startgame.clicked.connect(self.gamestart)

    def update(self):
        self.board = self._engine.getboard()
        self.view = self.board.tostring()

        c=0
        for i in self.view:
            c+=1
            self.ui.boardtest.insertPlainText(i)

            if c == self.board._width:
                self.ui.boardtest.append('')
                c=0


    def gamestart(self):
        self._engine.setgamestart(datetime.datetime.now())



    def renderBoard(self):
        pass









