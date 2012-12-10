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

        self.socket = socket
        self.clientNumber = clientNumber
        self.commandProcessor = commandProcessor
        self.threadDelay = threadDelay

        # create logger
        self._logger = NibbleStreamLogger("server.network.clientHandler.%d" % self.clientNumber, logging.INFO)

        try:
            self.listenThreadClientHandler = thread.start_new_thread(self.listen, (self.threadDelay,))
        except thread.error:
            self._logger.warning('Unable to start listenThreadClientHandler')

    def send(self, messageString):
        """Send messageString to the client.
                Arguments:
                    messageString -- (string)"""
        self._logger.info('"' + messageString + '" was sent to client')
        self.socket.sendall(messageString)

    def listen(self, delay):
        """Listens on the client.
                Arguments:
                    delay --  (integer) defined in seconds."""


        BUF_SIZE = 1024
        self.data = None
        while True:
            time.sleep(delay)
            try:
                self.data = self.socket.recv(BUF_SIZE)
            except Exception as e:
                self._logger.warning('Unable to receive data from client')
                #raise e

            if self.data:
                self._logger.info('Received: "' + self.data + '"')
                self.commandProcessor.receive(self.data, self.clientNumber)
                self.data = ''


if __name__ == "__main__":
    pass
