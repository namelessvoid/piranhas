from nibbles.server.network.server import Server
from nibbles.server.commandprocessor import CommandProcessor
from nibbles.server.engine import Engine

import random

commandprocessor = CommandProcessor()
server = Server(commandprocessor, '127.0.0.1', 1234, 1)
commandprocessor.setserver(server)
random = random.Random()
engine = Engine(random)
commandprocessor.setengine(engine)
engine.setcmp(commandprocessor)


while True:
    pass
