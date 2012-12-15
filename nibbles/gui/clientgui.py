from PyQt4 import QtGui, QtCore, uic
from datetime import datetime
from nibbles.nibblelogger import *

class ClientGui(QtGui.QMainWindow):
    def __init__(self, engine):
        QtGui.QMainWindow.__init__(self)
        self._ui = uic.loadUi("./nibbles/gui/clientgui.ui", self)
        self._engine = engine
        self._logger = NibbleQTextEditLogger(self._ui.logger, "client.gui")
        self._viewwidth = 5
        self._engine.registermethod(self.update)

        #get log messages from engine
        self._engine.initclientlogger(self._ui.logger)

        #startgame_btn gui
        self._ui.startgame.clicked.connect(self.gamestart)

        #stopgame_btn gui
        self._ui.stopgame.clicked.connect(self.gamestop)

    def update(self):
        view = self._engine.getcurrentview()
        if view:
            boardstring = ''
            for i in range(( len(view) / self._viewwidth )):
                i *= self._viewwidth
                boardstring += (view[i : self._viewwidth + i] + '\r\n')

            self._ui.field.setText(boardstring)
            self._ui.field.update()

    def gamestart(self):
        try:
            self._engine.connecttoserver(unicode(self._ui.ipInput.toPlainText()),
                int(unicode(self._ui.portInput.toPlainText())))
            self._engine.start()
            self._engine.sendcommand("anmeldung moeglich@")
        except:
            self._logger.warning("Cant connect to the server!")


    def gamestop(self):
        self._engine.stoploop()

    def renderBoard(self):
        pass










