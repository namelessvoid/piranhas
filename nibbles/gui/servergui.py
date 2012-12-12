import sys
from PyQt4 import QtGui, QtCore, uic
from logging import log

class ServerGui(QtGui.QMainWindow):
    def __init__(self, engine):
        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi("servergui.ui", self)

        for i in range(100):
            text = "Logger 08:08:2012 - INFO: Test logger" + str(i)
            self.ui.logger.append(text.rstrip())

        self._engine = engine
        self._engine.updatesignal.register(self.update)

    def update(self):
        pass





    def renderBoard(self):
        pass








if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    servergui = ServerGui()
    servergui.show()
    sys.exit(app.exec_())




