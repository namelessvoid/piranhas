import sys
from PyQt4 import QtGui, QtCore, uic
from logging import log
import datetime
from boardrenderer import BoardRenderer


class ServerGui(QtGui.QMainWindow):
    def __init__(self, engine):
        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi("./nibbles/gui/servergui.ui", self)

        self._boardrenderer = BoardRenderer()
        self._boardrenderer.repaint()

        for i in range(100):
            text = "Logger 08:08:2012 - INFO: Test logger" + str(i)
            self.ui.logger.append(text.rstrip())

        self._engine = engine
        self._engine.updatesignal.register(self.update)

        #startgame_btn gui
        self.ui.startgame.clicked.connect(self.gamestart)

        #stopgame_btn gui
        self.ui.stopgame.clicked.connect(self.gamestop)

    def update(self):
#        self.board = self._engine.getboard()
#        self.view = self.board.tostring()
#
#        self.boardsring = ''
#        for i in range(( len(self.view) / self.board._width )):
#            i *= self.board._width
#            self.boardsring += (self.view[i : self.board._width + i] + '\r\n')
#
#        self.ui.boardtest.setText(self.boardsring)
#        self.ui.boardtest.update()

        self._boardrenderer.repaint()


    def gamestart(self):
        self._engine.setgamestart(datetime.datetime.now())


    def gamestop(self):
        self._engine._endgame()











