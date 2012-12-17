import sys
from PyQt4 import QtGui, QtCore, uic
from logging import log
import datetime
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QMessageBox


class ServerGui(QtGui.QMainWindow):
    def __init__(self, engine):
        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi("./nibbles/gui/servergui.ui", self)

        for i in range(100):
            text = "Logger 08:08:2012 - INFO: Test logger" + str(i)
            self.ui.logger.append(text.rstrip())

        self._engine = engine



        #QMessage - about
        self.dialog = QtGui.QMessageBox("test", "test")

        #open about
        self.ui.about.activated.connect(self.aboutdialog)

        #connect to the update pattern
        self._engine.updatesignal.register(self.update)

        #startgame_btn gui
        self.ui.startgame.clicked.connect(self.gamestart)

        #stopgame_btn gui
        self.ui.stopgame.clicked.connect(self.gamestop)


    def update(self):
        self.c = 0
        if self.c == 0:
            self.ui.boardrenderer.setboard(self._engine.getboard())
            self.c+=1

        self.ui.boardrenderer.repaint()


    def gamestart(self):
        self._engine.setgamestart(datetime.datetime.now())
        self.ui.boardrenderer.setboard(self._engine.getboard())


    def gamestop(self):
        self._engine._endgame()


    def aboutdialog(self):
        self.dialog.show()