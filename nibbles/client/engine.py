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

    def recievecommand(self):
        """Recieves a message from networkinterface and return it"""
        command = self._ni.recieveMessage()
        return command

    def registrationpossible(self):
        """Checks whether registration is possible on server"""
        self._ni.sendMessage("anmeldung moeglich@")

    def connecttoserver(self):
        """Connects to the Server"""
        self._ni.sendMessage("anmelden@")

    def getworldsize(self):
        """Gets the size of the world"""
        self._ni.sendMessage("weltgroesse@")

    def startgame(self):
        """Starts the game"""
        self._ni.sendMessage("spielbeginn@")

    def movetoken(self, x, y, newX, newY):
        """Moves a token on the board"""
        self._board.moveToken(x, y, newX, newY)

    def settoken(self, token, x, y):
        """Sets a token on the board"""
        self._board.setToken(token, x, y)

    def gettoken(self, x, y):
        """Gets the token on the spezified position of the board"""
        self._board.getToken(x,y)

    def printmessage(self, message):
        """prints a message to stdout"""
        sys.stdout.write(message)

    def paintboard(self):
        """Renders the board"""
        self._board.paintBoard()

    def run(self):
        """Commandprocessor for the engine:
           in functions dictionary are server messages mapped to a function
           - ... : <function_name> => calls only the function without parameters
           - ... : (<function_name>,"") => calls the function with message from server as parameter
           - ... : (<function_name>,param) => calls the function with parameter param"""
        functions = {
            "ja@" : self.connecttoserver,
            "nein@" : (self.printmessage,"Anmeldung nicht moeglich"),
            "\D{1}@" : self.startgame,
            "\d+x\d+@" : (self.printmessage,""),
            "\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2}@" : (self.printmessage,"")
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
                self.printmessage("fehler@")
                break

if __name__== "__main__":
    sys.path.insert(0,"../")

    #brd = board.board(5,5)
    #ai = AI()

    engine = Engine()
    #engine.paintboard()
    engine.run()
