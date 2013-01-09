import sys
from PyQt4 import QtGui, QtCore, uic
from logging import log
import datetime

from nibbles.server.engine import RUNNING


class ServerGui(QtGui.QMainWindow):
    loggingsignal = QtCore.pyqtSignal(str)

    def __init__(self, engine):
        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi("./nibbles/gui/servergui.ui", self)
        self.ui.logger.setText("Logger")

        self._engine = engine

        #set window icon
        self.setWindowIcon(QtGui.QIcon('./nibbles/gui/img/logo_small.png'))

        #createaboutdialog
        self.createaboutdialog()

        #connect about
        self.ui.about.triggered.connect(self.aboutdialog)

        #connect to the update pattern
        self._engine.updatesignal.register(self.updategui)

        #startgame_btn gui
        self.ui.startgame.clicked.connect(self.gamestart)

        #stopgame_btn gui
        self.ui.stopgame.clicked.connect(self.gamestop)

        #timer for update of the lcd display
        self.lcdtimer = QtCore.QTimer()
        self.lcdtimer.timeout.connect(self.updatelcd)
        self.lcdtimer.start(1000)

        #register loggers
        self._registerloggers()

    def _registerloggers(self):
        """Called by __init__() and initializes the loggers."""
        self._engine._logger.logsignal.register(self.loggingsignal.emit)
        comp = self._engine._cmp
        comp._logger.logsignal.register(self.loggingsignal.emit)
        comp.server._logger.logsignal.register(self.loggingsignal.emit)
        self.loggingsignal.connect(self.ui.logger.logslot)

    def updategui(self):
        # Update nibbletree
        self.ui.nibbletree.clear()
        for nibble in self._engine._nibblelist:
            item = QtGui.QTreeWidgetItem(self.ui.nibbletree)
            item.setText(0, nibble.getname())
            item.setText(1, str(nibble.getenergy()))

        self.ui.boardrenderer.setboard(self._engine.getboard())
        self.ui.countdown.update()
        self.ui.boardrenderer.update()
        self.update()

    def gamestart(self):
        self._engine.setgamestart(datetime.datetime.now())
        self.ui.boardrenderer.setboard(self._engine.getboard())

    def gamestop(self):
        self._engine._endgame()

    def createaboutdialog(self):
        self.dialog = QtGui.QMessageBox()
        self.dialog.setWindowTitle("About - The Piranhas")
        self.dialog.setIconPixmap(QtGui.QPixmap("./nibbles/gui/img/title.png"))
        self.dialogtext = """About <hr/>
                            <p>Simon Kerler<br/>
                            Manuel Oswald<br/>
                            Benjamin Woehrl<br/>
                            Patrick Link<br/>
                            Christian Schmied</p>"""

        self.dialog.setText(self.dialogtext)

    def aboutdialog(self):
        self.dialog.show()

    def updatelcd(self):
        if self._engine.getgamestatus() == RUNNING:
            self.ui.countdown.display(self._engine._currentround)
            self.ui.countdownlabel.setText("Round:")
            return 0
        time = self._engine._gamestart - datetime.datetime.now()
        h = time.seconds / 3600
        m = (time.seconds % 3600) / 60
        s = (time.seconds % 60)
        text = "%02i:%02i:%02i" % (h, m, s)
        self.ui.countdown.display(text)

