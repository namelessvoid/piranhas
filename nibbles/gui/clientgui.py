from PyQt4 import QtGui, QtCore, uic
from datetime import datetime
from nibbles.nibblelogger import *
from nibbles.board import *

class ClientGui(QtGui.QMainWindow):
    def __init__(self, engine):
        QtGui.QMainWindow.__init__(self)
        self._ui = uic.loadUi("./nibbles/gui/clientgui.ui", self)
        self._engine = engine
        self._logger = NibbleQTextEditLogger(self._ui.logger, "client.gui")

        #register the update method for gui
        self._engine.registermethod(self.updategui)

        #get log messages from engine
        self._engine.initclientlogger(self._ui.logger)

        #startgame_btn gui
        self._ui.startgame.clicked.connect(self.gamestart)

        #stopgame_btn gui
        self._ui.stopgame.clicked.connect(self.gamestop)

    def updategui(self):
#        view = self._engine.getcurrentview()
#        if view:
#            boardstring = ''
#            for i in range(( len(view) / self._viewwidth )):
#                i *= self._viewwidth
#                boardstring += (view[i : self._viewwidth + i] + '\r\n')
#
#            self._ui.field.setText(boardstring)
#            self._ui.field.update()

        board = createfromstring(self._engine.getcurrentview(), 5)
        self._ui.boardrenderer.setboard(board)

        self._ui.boardrenderer.update()
        self.update()

    def gamestart(self):
        try:
            host, okhost = QtGui.QInputDialog.getText(self, "Host Settings", "Host:")
            if not okhost: return
            port, okport = QtGui.QInputDialog.getInt(self, "Port Settings", "Port:")
            if not okport: return
            self._logger.info("Host: %s" % host)
            self._logger.info("Port: %d" % port)
            self._engine.connecttoserver(host, port)
            self._engine.start()
            self._engine.sendcommand("anmeldung moeglich@")
        except:
            self._logger.warning("Cant connect to the server!")

    def gamestop(self):
        self._engine.stoploop()










