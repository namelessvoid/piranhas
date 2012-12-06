from nibbles.server.network.clientHandler import ClientHandler
from nibbles.nibblelogger import NibbleStreamLogger

import socket
import threading
import logging


class Server():
    def __init__(self, commandProcessor, HOST, PORT, threadDelay):
        """Initializes the server.
                Arguments:
                    commandProcessor -- (CommandProcessor)
                    HOST -- (string)
                    PORT -- (integer)
                    threadDelay -- (integer) This is the number of seconds execution to be suspended"""

        # create logger
        self._logger = NibbleStreamLogger("server.network.server", logging.INFO)

        self.commandProcessor = commandProcessor
        self.clientList = []

        try:
            self.listenThreadServer = threading.Thread(target=self.listen, args=(HOST, PORT, threadDelay))
            self.listenThreadServer.start()
            self._logger.info('Serverthread started!')
        except:
            self._logger.warning('Unable to start listenThreadServer')

    def setjoin(self):
        self.listenThreadServer.join()

    def listen(self, HOST='', PORT=1234, threadDelay=1):
        """Listens to the socket.
                Arguments:
                    HOST --  (string).
                    PORT --  (integer).
                    delay -- (integer) This is the number of seconds execution to be suspended"""
        self.threadDelay = threadDelay
        self.HOST = HOST
        self.PORT = PORT
        self.clientNumber = 0

        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.s.bind((self.HOST, self.PORT))
        except:
            self._logger.warning('Unable to bind HOST and PORT to the socket!')

        self._logger.info("Serversocket .bind succeeded: HOST %s, PORT %s)"  %(self.HOST, self.PORT))
        self.s.listen(1)

        while True:
            c, (clienthost, clientport) = self.s.accept()
            logging.info('Verbunden mit %s:%d' % (clienthost, clientport))
            self.clientList.insert(self.clientNumber ,ClientHandler(self.commandProcessor, c, self.clientNumber, self.threadDelay))
            self.clientNumber += 1

    def sendTo(self, currentClientNumber=0, message=''):
        """Sends messages to the specific client.
                Arguments:
                    currentClientNumber -- (integer)
                    message -- (string) """
        self.clientList[currentClientNumber].send(message)



if __name__ == "__main__":
    pass
