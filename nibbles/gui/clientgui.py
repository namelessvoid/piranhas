from PyQt4 import QtGui, QtCore, uic
from datetime import datetime
from nibbles.nibblelogger import *
from nibbles.board import *

class ClientGui(QtGui.QMainWindow):
    loggingsignal = QtCore.pyqtSignal(str)

    def __init__(self, engine):
        QtGui.QMainWindow.__init__(self)
        self._ui = uic.loadUi("./nibbles/gui/clientgui.ui", self)
        self._engine = engine

        self._logger = NibbleStreamLogger("gui.clientgui")

        #register logging text box to the engine logger.
        self._engine._logger.logsignal.register(self.loggingsignal.emit)
        self._engine._ni._logger.logsignal.register(self.loggingsignal.emit)
        self._logger.logsignal.register(self.loggingsignal.emit)
        self._ui.logger.setText("Logger")
        self.loggingsignal.connect(self._ui.logger.logslot)

        #register the update method for gui
        self._engine.registermethod(self.updategui)

        #startgame_btn gui
        self._ui.startgame.clicked.connect(self.showdialog)

        #stopgame_btn gui
        self._ui.stopgame.clicked.connect(self.gamestop)

        #create input dialog
        self.createinputdialog()

    def updategui(self):
        self._ui.boardrenderer.setboard(self._engine.getcurrentboard())
        self._ui.boardrenderer.update()
        self.update()

    def gamestart(self):
        try:
            QtGui.QMessageBox.close(self._dialog)
            host = self._hostinput.text()
            port = int(self._portinput.text())
            self._engine.connecttoserver(host, port)
            self._engine.start()
            self._engine.sendcommand("anmeldung moeglich@")
        except:
            self._logger.warning("Cant connect to the server!")

    def createinputdialog(self):
        """Creates a dialog for host and port settings"""
        self._dialog = QtGui.QDialog()
        self._dialog.setWindowTitle("Settings")
        but = QtGui.QPushButton("OK")
        self._hostinput = QtGui.QLineEdit()
        self._portinput = QtGui.QLineEdit()
        layout = QtGui.QVBoxLayout()
        layout.addWidget(QtGui.QLabel("Host:"))
        layout.addWidget(self._hostinput)
        layout.addWidget(QtGui.QLabel("Port:"))
        layout.addWidget(self._portinput)
        layout.addWidget(but)
        self._dialog.setLayout(layout)
        self._dialog.connect(but, QtCore.SIGNAL("clicked()"), self.gamestart)

    def showdialog(self):
        self._dialog.show()

    def gamestop(self):
        self._engine.stoploop()
