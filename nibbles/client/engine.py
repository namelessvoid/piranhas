""" Client Engine for managing communication between networkinterface, board and AI """

import re
import sys
import time
import threading
from socket import *
from nibbles.nibblelogger import *
from nibbles.board import *
from nibbles.client.ai import *
from nibbles.client.network.networkinterface import *

class DummyServer(threading.Thread): #to be removed
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self._b = Board(10,10)
        self._s = socket.socket()
        self._s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._s.bind((host,port))
        self._s.listen(1)
        self.start()

    def run(self):
        c, (clienthost, clientport) = self._s.accept()
        c.sendall("30;..*....*.>..A....<..*..*.;@")
        data = c.recv(1024)
        print("Vom Server: "+data+"\n")

class DummyClient(): #to be removed
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.verbinden()

    def verbinden(self):
        self._s.connect((self._host,self._port))

    def receivemessage(self):
        return self._s.recv(1024)

    def sendmessage(self, message):
        self._s.sendall(message)




class Engine(threading.Thread):

    def __init__(self, ni=None, renderer=None, ai=None):
        """Init the Engine"""
        threading.Thread.__init__(self)
        self._ni = ni
        self._renderer = renderer
        self._ai = ai
        self._gamerun = True
        self._currentview = ""
        self._updatemethod = None
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

    def renderboard(self, view, energy):
        """Renders the board"""
        #self._renderer.renderboard(view, energy)

    def stoploop(self):
        """Stops the gameloop"""
        self._gamerun = False

    def getcurrentview(self):
        """Returns the actual view of the nibble"""
        return self._currentview

    def registermethod(self, function):
        """Register a function which will be called in the gameloop"""
        self._updatemethod = function

    def updategui(self):
        if self._updatemethod != None:
            self._updatemethod()

    def handlemessage(self, message):
        """Handles the message from the server"""
        energy = message.split(";")[0]
        view = message.split(";")[1]
        field = message.split(";")[2]
        if view != "ende":
            self._currentview = view
            self.sendcommand( str( self._ai.think(view, energy) )+"@" )
        else:
            self.stoploop()

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
                        break

            self.updategui()
            time.sleep(0.4)

if __name__== "__main__":

    #server = DummyServer('', 1234)
    #client = DummyClient("localhost", 1234)
    client = NetworkInterface("localhost", 1234)
    board = Board(10,10)
    ai = AI()

    #ni = NetworkInterface("localhost", 1234)

    engine = Engine(client, board, ai)
    engine.start()
    engine.sendcommand("anmeldung moeglich@")
