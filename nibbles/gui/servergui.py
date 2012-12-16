import sys
from PyQt4 import QtGui, QtCore, uic
from logging import log
import datetime
from boardrenderer import BoardRenderer


class ServerGui(QtGui.QMainWindow):
    def __init__(self, engine):
        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi("./nibbles/gui/servergui.ui", self)

        for i in range(100):
            text = "Logger 08:08:2012 - INFO: Test logger" + str(i)
            self.ui.logger.append(text.rstrip())

        self._engine = engine

        #boardrenderer widget
        self._boardrenderer = BoardRenderer()

        #connect to the update pattern
        self._engine.updatesignal.register(self.update)

        #startgame_btn gui
        self.ui.startgame.clicked.connect(self.gamestart)

        #stopgame_btn gui
        self.ui.stopgame.clicked.connect(self.gamestop)


    def update(self):
        self._boardrenderer.repaint()


    def gamestart(self):
        self._engine.setgamestart(datetime.datetime.now())


    def gamestop(self):
        self._engine._endgame()
