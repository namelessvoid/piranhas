from PyQt4 import QtGui, QtCore
import sys
from nibbles.client.engine import *
from nibbles.client.ai import *
from nibbles.client.network.networkinterface import *
from nibbles.gui.clientgui import ClientGui

ai = AI()
ni = NetworkInterface()
engine = Engine(ni, None, ai)
app = QtGui.QApplication(sys.argv)
clientgui = ClientGui(engine)
clientgui.show()
sys.exit(app.exec_())

