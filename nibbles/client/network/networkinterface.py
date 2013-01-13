""" The client's network interface.

    The network interface takes strings from the engine and sends them to the
    socket which esatblished the connection to the server.
    Also it receives messages from the server and hands them over to the
    engine."""

import socket, thread, time
from nibbles.nibblelogger import *

class NetworkInterface(socket.socket):
    #_s, _host, _port = (None, None, None)

    def __init__(self):
        """Initialize the NetworkInterface
        host:    string that holds the address of the host
        port:    integer that holds the destination port"""
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM)
        self._inbuffer = []
        self._outbuffer = []
        self._logger = NibbleStreamLogger("client.networkinterface")

    def connecttoserver(self, host, port):
        self.connect((host, port))
        self._logger.info("NetworkInterface connected to %s:%d" % (host, port))
        try:
            self.receivemessageThread = thread.start_new_thread(self.receivemessage, ())
        except thread.error:
            self._logger.info("Error at connection, cant start thread")

    def sendmessage(self, message):
        """Sends a message to the host.
        message: string representation of the message."""
        self._outbuffer.append(message)
        self._logger.info("NetworkInterface.sendMessage(\"" + message + "\")")
        #socketfile = self.makefile()
        #socketfile.write(message)
        while len(self._outbuffer) > 0:
            self.send(self._outbuffer.pop())
        #logging.info("NetworkInterface.sendMessage() DONE")
        #socketfile.close()

    def clearbuffers(self):
        del self._inbuffer[:]
        del self._outbuffer[:]

    def getmessage(self):
        if len(self._inbuffer) > 0:
            return self._inbuffer.pop()
        else:
            return False

    def receivemessage(self):
        """Receives a message from the host.
        return value: String which holds the message"""
        self._logger.info("NetworkInterface().receiveMessage()")
        try:
            while 1:
                data = self.recv(1024)
                if not data:
                    break
                self._logger.info("received: " + str(data))
                self._inbuffer.append(data)
        except socket.error, (errno, string):
            self._logger.info("Error at receiving a message")


if __name__ == "__main__":
    ni = NetworkInterface("localhost", 50007)
    ni.sendMessage("Hallo!\n")
    print ni.receiveMessage()
