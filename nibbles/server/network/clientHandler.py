import thread
import time
import logging
from nibbles.nibblelogger import NibbleStreamLogger

class ClientHandler():
    def __init__(self, commandProcessor, socket, clientNumber=0, threadDelay=1):
        """Initialize the ClientHandler.
                Arguments:
                    commandProcessor -- (CommandProcessor)
                    socket -- (Socket)
                    clientNumber -- (integer) individual number of the client
                    threadDelay -- (integer) This is the number of seconds execution to be suspended. """

        # create logger
        self._logger = NibbleStreamLogger("server.network.clientHandler", logging.INFO)

        self.socket = socket
        self.clientNumber = clientNumber
        self.commandProcessor = commandProcessor
        self.threadDelay = threadDelay

        try:
            self.listenThreadClientHandler = thread.start_new_thread(self.listen, (self.threadDelay,))
        except thread.error:
            self._logger.warning('Unable to start listenThreadClientHandler %s' % self.clientNumber)

    def send(self, messageString):
        """Send messageString to the client.
                Arguments:
                    messageString -- (string)"""
        self._logger.info('"' + messageString + '"' + ' was sent to client with the id ' + str(self.clientNumber))
        self.socket.sendall(messageString)

    def listen(self, delay):
        """Listens on the client.
                Arguments:
                    delay --  (integer) defined in seconds."""

        try:
            BUF_SIZE = 1024
            self.data = None
            while True:
                time.sleep(delay)
                self.data = self.socket.recv(BUF_SIZE)
                if self.data:
                    self._logger.info('Received: ' + self.data)
                    self.commandProcessor.receive(self.data, self.clientNumber)
                    self.data = ''
        except Exception as e:
            self._logger.warning('Unable to receive data.')
            raise e

if __name__ == "__main__":
    pass
