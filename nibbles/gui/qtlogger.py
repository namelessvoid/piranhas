# -*- coding: utf-8 *-*

from PyQt4.QtGui import QTextEdit


class QtLogger(QTextEdit):
    def __init__(self, parent = None):
        QTextEdit.__init__(self, parent)
        self._logtext = ""

    def logslot(self, message):
        self.append(message)
        pass
