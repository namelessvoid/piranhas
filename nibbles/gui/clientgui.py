from PyQt4 import QtGui, QtCore, uic
from datetime import datetime

class ClientGui(QtGui.QMainWindow):
    def __init__(self, engine):
        QtGui.QMainWindow.__init__(self)
        self._ui = uic.loadUi("./nibbles/gui/clientgui.ui", self)
        self._engine = engine
        self._viewwidth = 5
        self._engine.registermethod(self.update)

        #startgame_btn gui
        self._ui.startgame.clicked.connect(self.gamestart)

        #stopgame_btn gui
        self._ui.stopgame.clicked.connect(self.gamestop)

    def update(self):
        view = self._engine.getcurrentview()
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
            self._ui.logger.append(str(datetime.now())+": Connected to the server")
            self._engine.start()
            self._engine.sendcommand("anmeldung moeglich@")
            self._ui.logger.append(str(datetime.now())+": Registered...")
        except:
            self._ui.logger.append(str(datetime.now())+": Cant connect to the server!")


    def gamestop(self):
        self._engine.stoploop()
        self._ui.logger.append(str(datetime.now())+": Game stopped")


    def renderBoard(self):
        pass










