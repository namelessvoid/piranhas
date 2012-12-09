from ConfigParser import RawConfigParser
from datetime import datetime
import random

from nibbles.server.network.server import Server
from nibbles.server.commandprocessor import CommandProcessor
from nibbles.server.engine import Engine

# read in the configuration file.
configparser = RawConfigParser()
configparser.read("server.cfg")

port = configparser.getint("network", "port")
host = configparser.get("network", "host")
starttime = configparser.get("engine", "starttime")
starttime = datetime.strptime(starttime, "%y.%m.%d/%H:%M:%S")
foodpernibble = configparser.getint("engine", "foodpernibble")
fieldspernibble = configparser.getint("engine", "fieldspernibble")

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
engine.setgamestart(starttime)

# run the server
server.setjoin()
