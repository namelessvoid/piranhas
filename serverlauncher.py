from ConfigParser import RawConfigParser
from datetime import datetime
import random
from PyQt4 import QtGui, QtCore
import sys

from nibbles.server.network.server import Server
from nibbles.server.commandprocessor import CommandProcessor
from nibbles.server.engine import Engine
from nibbles.gui.servergui import ServerGui

# read in the configuration file.
configparser = RawConfigParser()
configparser.read("server.cfg")

port = configparser.getint("network", "port")
host = configparser.get("network", "host")
starttime = configparser.get("engine", "starttime")
starttime = datetime.strptime(starttime, "%y.%m.%d/%H:%M:%S")
foodpernibble = configparser.getint("engine", "foodpernibble")
fieldspernibble = configparser.getint("engine", "fieldspernibble")
turntimeout = configparser.getint("engine", "turntimeout")
rounds = configparser.getint("engine", "rounds")

# instantiate objects
commandprocessor = CommandProcessor(starttime)
server = Server(commandprocessor, host, port, 1)
commandprocessor.setserver(server)
random = random.Random()
engine = Engine(random)

# set up configurations
commandprocessor.setengine(engine)
engine.setcmp(commandprocessor)

engine.setfoodpernibble(foodpernibble)
engine.setfieldspernibble(fieldspernibble)
engine.setturntimeout(turntimeout)
engine.setgamestart(starttime)
engine.setrounds(rounds)

# run the server
#server.setjoin()

app = QtGui.QApplication(sys.argv)
servergui = ServerGui(engine)
servergui.show()
sys.exit(app.exec_())
