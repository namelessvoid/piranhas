import logging
from nibbles.server.serverexceptions import *
from nibbles.server.engine import INIT
from nibbles.nibblelogger import NibbleStreamLogger

class CommandProcessor():
    def __init__(self, gamestarttime):
        """Initialize the CommandProcessor."""

        self.nibbleclientdict = {}
        self.engine = None
        self.server = None
        self.gamestarttime = gamestarttime

    def setserver(self, server):
        """Receives the instanz of the server and stores it.
                Arguments:
                    server -- (Server)"""
        self.server = server

    def setengine(self, engine):
        """Receives the instanz of the engine and stores it.
                Arguments:
                    engine -- (Engine)"""
        self.engine = engine

    def receive(self, data, clientNumber):
        """Receives and handles the messages from the clients.
                Arguments:
                    data --  (string).
                    clientNumber --  (integer)"""

        data = data.strip()

        if data == 'anmeldung moeglich@':
            if self.engine.getgamestatus() == INIT:
                    self.server.sendTo(clientNumber, 'ja@')
            else:
                    self.server.sendTo(clientNumber, 'nein@')
        elif data == 'anmelden@':
            if clientNumber in self.nibbleclientdict:
                self.server.sendTo(clientNumber, 'fehler@')
            else:
                nibblechar = None
                try:
                    nibblechar = self.engine.register()
                    self.nibbleclientdict[nibblechar] = clientNumber
                except RegisterNibbleFailedException, m:
                    logging.warning(m)
                    logging.warning('Anmeldung von %d mit Buchstabe %s nicht moeglich!' %(clientNumber,nibblechar))
                if nibblechar != None:
                    self.server.sendTo(clientNumber, '%s@' %nibblechar)

        elif clientNumber in self.nibbleclientdict:
            if data == 'weltgroesse@':
                if self.engine.getgamestatus() == INIT:
                    self.server.sendTo(clientNumber, 'fehler@')
                else:
                    x, y = self.engine.getworlddimentions()
                    self.server.sendTo(clientNumber, '%dx%d@' %x, y)

            elif data == 'spielbeginn@':
                self.server.sendTo(clientNumber, self.gamestarttime)

            elif 2 <= len(data) <= 3:
                directionnumber = None
                if '@' in data:
                    directionnumber = data.strip("@")
                    if 0 >= directionnumber <= 24:
                        for value in self.nibbleclientdict.items():
                            if value[1] == clientNumber:
                                self.nibbleid = value[0]

                            if self.engine.execturn(self.nibbleid, directionnumber) == -1:
                                self._logger.warning('')
                                self.server.sendTo(clientNumber, 'fehler@')
                            else:
                                self._logger.info('Movement succeeded!')

                    else:
                        self.server.sendTo(clientNumber, 'fehler@')

        else:
            self.server.sendTo(clientNumber,'fehler@')


    def send(self, nibbleid, board, energy, end = 'false'):
        """Forwards the board, energy and the end to server.sendTo
                Arguments:
                    nibbleid -- (integer)
                    board -- (Board)
                    energy -- (integer)
                    end -- (boolean)"""
        if energy <= 0:
            self.server.sendTo(self.nibbleclientdict[nibbleid], ';;@')
        elif end:
            self.server.sendTo(self.nibbleclientdict[nibbleid], '%d;ende;%s@' %(energy, board))
        else:
            self.server.sendTo(self.nibbleclientdict[nibbleid], '%d;%s;@' %(energy,  board))



if __name__ == "__main__":
    pass