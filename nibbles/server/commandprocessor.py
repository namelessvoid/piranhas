import logging

class CommandProcessor():

    def __init__(self):
        """Initialize the commandProcessor."""

        self.nibbleclientdict = {}
        self.engine = None
        self.server = None

    def setserver(self, server):
        """Receives the instanz of the server and stores it.
                Arguments:
                    server -- (server)"""
        self.server = server

    def setengine(self, engine):
        """Receives the instanz of the engine and stores it.
                Arguments:
                    engine -- (engine)"""
        self.engine = engine

    def receive(self, data, clientNumber):
        """Receives and handles the messages from the clients.
                Arguments:
                    data --  (integer) defined in seconds.
                    clientNumber --  (string) defined in seconds."""

        if data == 'anmeldung moeglich@':
            if self.engine.getgamestatus() == self.engine.INIT:
                    self.server.sendTo(clientNumber, 'ja@')
            else:
                    self.server.sendTo(clientNumber, 'nein@')
        elif data == 'anmelden@':
            if clientNumber in self.nibbleclientdict:
                self.server.sendTo(clientNumber, 'fehler@')
            else:
                nibblechar = None
                try:
                    nibblechar = self.engine.registernibble()
                    self.nibbleclientdict[nibblechar] = clientNumber
                except:
                    logging.warning('Anmeldung von %d mit Buchstabe %s nicht moeglich!' %(clientNumber,nibblechar))
                if nibblechar != None:
                    self.server.sendTo(clientNumber, '%s@' %nibblechar)

        elif clientNumber in self.nibbleclientdict:
            if data == 'weltgroesse@':
                if self.engine.getgamestatus() == self.engine.INIT:
                    self.server.sendTo(clientNumber, 'fehler@')
                else:
                    x, y = self.engine.getworlddimentions()
                    self.server.sendTo(clientNumber, '%dx%d@' %x, y)

            elif data == 'spielbeginn@':
                self.server.sendTo(clientNumber, self.configloader.getgamestartime())

            elif 2 <= len(data) <= 3:
                directionnumber = None
                if '@' in data:
                    directionnumber = data.strip("@")
                    if 0 >= directionnumber <= 24:
                        #if self.engine.getcurrentnibbleid() == self.nibbleclientdict. :
                            #self.nibbleclientdict.values().index(clientNumber)
                        pass
                    else:
                        self.server.sendTo(clientNumber, 'fehler@')

        else:
            self.server.sendTo(clientNumber,'fehler@')


    def send(self, nibbleid, board, energy, end = 'false'):
        """Receives the instanz of the server and stores it.
                Arguments:
                    nibbleid -- (integer)
                    board -- ()
                    energy -- (integer)
                    end -- (boolean)"""
        if energy <= 0:
            self.server.sendTo(self.nibbleclientdict[nibbleid], ';;@')
        elif end:
            self.server.sendTo(self.nibbleclientdict[nibbleid], '%d;ende;%s@' %energy %board)
        else:
            self.server.sendTo(self.nibbleclientdict[nibbleid], '%d;%s;@' %energy %board)



if __name__ == "__main__":
    pass