import socket
import logging
import thread
from nibbles.server.network.clientHandler import ClientHandler



class Server():
    def __init__(self, commandProcessor, HOST, PORT, threadDelay):
        """Initializes the server.
                Arguments:
                    commandProcessor -- (commandprocessor)
                    HOST -- (integer)
                    PORT -- (integer)
                    threadDelay -- (integer) This is the number of seconds execution to be suspended"""
        print ("Instantiating server.")
        self.commandProcessor = commandProcessor
        self.clientList = []

        try:
            self.listenThreadServer = thread.start_new_thread(self.listen, (HOST, PORT, threadDelay))
        except thread.error:
            logging.warning('Unable to start listenThreadServer')

        while True:
            pass


    def listen(self, HOST='', PORT=1234, threadDelay=1):
        """Listens to the socket.
                Arguments:
                    HOST --  (integer).
                    PORT --  (integer).
                    delay -- (integer) This is the number of seconds execution to be suspended"""
        print ("Initialize listen thread")
        self.threadDelay = threadDelay
        self.HOST = HOST
        self.PORT = PORT
        self.clientNumber = 0
        print "adas"

        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.HOST, self.PORT))
        self.s.listen(1)

        print "lksdf"

        while True:
            self.clientNumber += 1
            c, (clienthost, clientport) = self.s.accept()
            logging.info('Verbunden mit %s:%d' % (clienthost, clientport))
            self.clientList.insert(self.clientNumber ,ClientHandler(self.commandProcessor, c, self.clientNumber, self.threadDelay))

    def sendTo(self, currentClientNumber=0, message=''):
        """Sends messages to the specific client.
                Arguments:
                    currentClientNumber -- (integer)
                    message -- (string) """
        self.clientList[currentClientNumber].send(message)



if __name__ == "__main__":
    pass
