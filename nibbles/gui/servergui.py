import sys
from PyQt4 import QtGui, QtCore, uic
from logging import log

class ServerGui(QtGui.QMainWindow):
    def __init__(self):
        app = QtGui.QApplication(sys.argv)
        self.ui = uic.loadUi("servergui.ui")
        self.ui.show()

        i = 0
        while i < 100:
            text = "Logger 08:08:2012 - INFO: Test logger" + str(i)
            self.ui.logger.append(text.rstrip())
            i += 1

        sys.exit(app.exec_())


#    def log(self, text):
#        # Write into the log window and remove "\n" if necessary
#        self.ui.logger.append(text)
#
#        # Scroll to the end
#        cursor = self.ui.logTextEdit.textCursor()
#        cursor.movePosition(QTextCursor.End)
#        self.ui.logTextEdit.setTextCursor(cursor)

if __name__ == "__main__":
    servergui = ServerGui()
