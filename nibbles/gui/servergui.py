import sys
from PyQt4 import QtGui, QtCore, uic
from logging import log
import datetime

import datetime
from boardrenderer import BoardRenderer
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
        self._engine.updatesignal.register(self.updategui)

        #startgame_btn gui
        self.ui.startgame.clicked.connect(self.gamestart)

        #stopgame_btn gui
        self.ui.stopgame.clicked.connect(self.gamestop)

        #tmer for update of the lcd display
        self.lcdtimer = QtCore.QTimer()
        self.lcdtimer.timeout.connect(self.updatelcd)
        self.lcdtimer.start(1000)

    def updategui(self):
        self.c = 0
        if self.c == 0:
            self.ui.boardrenderer.setboard(self._engine.getboard())
            self.c += 1

        self.ui.boardrenderer.update()
        self.update()


    def gamestart(self):
        self._engine.setgamestart(datetime.datetime.now())
        self.ui.boardrenderer.setboard(self._engine.getboard())


    def gamestop(self):
        self._engine._endgame()


    def aboutdialog(self):
        self.dialog.show()
    def updatelcd(self):
        time = self._engine._gamestart - datetime.datetime.now()
        h = time.seconds / 3600
        m = (time.seconds % 3600) / 60
        s = (time.seconds % 60)
        text = "%02i:%02i:%02i" % (h, m, s)
        self.ui.countdown.display(text)

