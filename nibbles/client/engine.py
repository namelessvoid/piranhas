""" Client Engine for managing communication between networkinterface, board and AI """

import re
import sys
import time
import threading
from nibbles.nibblelogger import *
from nibbles.board import *
from nibbles.client.ai import *
from nibbles.client.network.networkinterface import *

class Engine(threading.Thread):

    def __init__(self, ni=None, ai=None):
        """Init the Engine"""
        threading.Thread.__init__(self)
        self._ni = ni
        self._currentboard = None
        self._currentenergy = None
        self._ai = ai
        self._gamerun = True
        self._updatemethods = {}
        self._logger = NibbleStreamLogger("client.engine")

    def receivecommand(self):
        """Recieves a message from networkinterface and return it"""
        return self._ni.getmessage()

    def sendcommand(self, command):
        self._ni.sendmessage(command)

    def registrationpossible(self):
        """Checks whether registration is possible on server"""
        self._ni.sendmessage("anmeldung moeglich@")

    def connecttoserver(self, host, port):
        """Connects to the Server"""
        self._ni.connecttoserver(host, port)

    def register(self):
        """Register nibble"""
        self._ni.sendmessage("anmelden@")

    def getworldsize(self):
        """Gets the size of the world"""
        self._ni.sendmessage("weltgroesse@")

    def startgame(self):
        """Starts the game"""
        self._ni.sendmessage("spielbeginn@")

    def printmessage(self, message):
        """prints a message to stdout"""
        sys.stdout.write(message)

    def stoploop(self):
        """Stops the gameloop"""
        self._gamerun = False

    def getgamestatus(self):
        """Returns the current status of the game"""
        return self._gamerun

    def getcurrentboard(self):
        """Returns the actual view of the nibble"""
        return self._currentboard

    def getcurrentenergy(self):
        """Returns the actual view of the nibble"""
        return self._currentenergy

    def registermethods(self, functions):
        """Register some functions which will be called from engine"""
        self._updatemethods = functions

    def updategui(self):
        if self._updatemethods["updategui"]:
            self._updatemethods["updategui"]()

    def handlemessage(self, message):
        """Handles the message from the server"""
        energy = message.split(";")[0]
        view = message.split(";")[1]
        field = message.split(";")[2]
        self._currentenergy = energy
        if view != "ende" and int(energy) > 0:
            self._currentboard = createfromstring(view, 5, 5)
            self.sendcommand( str( self._ai.think(view, energy) )+"@" )
        else:
            self._logger.info(" Game Over!")
            self._updatemethods["gameoverdialog"]()

    def run(self):
        """Commandprocessor for the engine:
           in functions dictionary are server messages mapped to a function"""

        functions = {
            "ja@" : lambda param: self.register(),
            "nein@" : lambda param: self.printmessage("Anmeldung nicht moeglich"),
            "\D{1}@" : lambda param: self.startgame(),
            "\d+x\d+@" : lambda param: self.printmessage(param),
            "\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2}" : lambda param: self.printmessage(param), #do something
            "(;|\d{1,4};)(;|[*><=.\D]{25};|ende;)(@|[*><=.\D]*@)" : lambda param: self.handlemessage(param)
        }

        while self._gamerun:
            command = self.receivecommand()
            time.sleep(0.3)
            if command:
                self._logger.info(" Client Received command: %s" % command)

                for i, key in enumerate(functions):
                    if re.match(key, command):
                        functions[key](command)
                        break
                    elif i == len(functions) - 1:
                        self.printmessage("fehler@\n")
                        self._logger.warning(" Unknown command: %s" % command)
                        break

            self.updategui()
            time.sleep(0.4)

if __name__== "__main__":

    client = NetworkInterface()
    ai = AI()

    engine = Engine(client, None, ai)
    engine.connecttoserver("localhost", 1234)
    engine.start()
    engine.sendcommand("anmeldung moeglich@")
