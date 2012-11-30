""" Client Engine for managing communication between networkinterface, board and AI """

import re
import sys
import threading

class Engine(threading.Thread):

    def __init__(self, ni=None, board=None, ai=None):
        """Init the Engine"""
        threading.Thread.__init__(self)
        self._ni = ni
        self._board = board
        self._ai = ai

    def recieveCommand(self):
        """Recieves a message from networkinterface and return it"""
        command = self._ni.recieveMessage()
        return command

    def registrationPossible(self):
        """Checks whether registration is possible on server"""
        self._ni.sendMessage("anmeldung moeglich@")

    def connectToServer(self):
        """Connects to the Server"""
        self._ni.sendMessage("anmelden@")

    def getWorldSize(self):
        """Gets the size of the world"""
        self._ni.sendMessage("weltgroesse@")

    def startGame(self):
        """Starts the game"""
        self._ni.sendMessage("spielbeginn@")

    def moveToken(self, x, y, newX, newY):
        """Moves a token on the board"""
        self._board.moveToken(x, y, newX, newY)

    def setToken(self, token, x, y):
        """Sets a token on the board"""
        self._board.setToken(token, x, y)

    def getToken(self, x, y):
        """Gets the token on the spezified position of the board"""
        self._board.getToken(x,y)

    def printMessage(self, message):
        """prints a message to stdout"""
        sys.stdout.write(message)

    def paintBoard(self):
        """Renders the board"""
        self._board.paintBoard()

    def run(self):
        """Commandprocessor for the engine:
           in functions dictionary are server messages mapped to a function
           - ... : <function_name> => calls only the function without parameters
           - ... : (<function_name>,"") => calls the function with message from server as parameter
           - ... : (<function_name>,param) => calls the function with parameter param"""
        functions = {
            "ja@" : self.connectToServer,
            "nein@" : (self.printMessage,"Anmeldung nicht moeglich"),
            "\D{1}@" : self.startGame,
            "\d+x\d+@" : (self.printMessage,""),
            "\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2}@" : (self.printMessage,"")
        }
        #while 1:
        #command = self.recieveCommand()
        command = "2012-11-17 00:00:00@"
        for i, key in enumerate(functions):
            if command == key:
                if isinstance(functions[command], tuple):
                    func, param = functions[command]
                    if param == "":
                        func(command)
                    else:
                        func(param)
                    break
                else:
                    functions[command]()
                    break
            elif re.match(key, command):
                if isinstance(functions[key], tuple):
                    func, param = functions[key]
                    if param == "":
                        func(command)
                    else:
                        func(param)
                    break
                else:
                    functions[key]()
                    break
            elif i == len(functions)-1:
                self.printMessage("fehler@")
                break

if __name__== "__main__":
    sys.path.insert(0,"../")

    #brd = board.board(5,5)
    #ai = AI()

    engine = Engine()
    #engine.paintBoard()
    engine.run()
