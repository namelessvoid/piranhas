""" The client's network interface.

    The network interface takes strings from the engine and sends them to the
    socket which esatblished the connection to the server.
    Also it receives messages from the server and hands them over to the
    engine."""

import socket
import logging
import thread
from nibbles.nibblelogger import *

class NetworkInterface(socket.socket):
    #_s, _host, _port = (None, None, None)

    def __init__(self, host, port):
        """Initialize the NetworkInterface
        host:    string that holds the address of the host
        port:    integer that holds the destination port"""
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM)
        self._buffer = False
        self._host = host
        self._port = port
        self._logger = NibbleStreamLogger("client.networkinterface")
        self.connect((self._host, self._port))
        self._logger.info("NetworkInterface connected to %s:%d" % (host, port))
        try:
            self.receivemessageThread = thread.start_new_thread(self.receivemessage, ())
        except thread.error:
            self._logger.info("Error at connection, cant start thread")

    def sendmessage(self, message):
        """Sends a message to the host.
        message: string representation of the message."""
        self._logger.info("NetworkInterface.sendMessage(\"" + message + "\")")
        socketfile = self.makefile()
        socketfile.write(message)
        #logging.info("NetworkInterface.sendMessage() DONE")
        socketfile.close()

    def getmessage(self):
        if self._buffer:
            tmp = self._buffer
            self._buffer = False
            return tmp
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
                self._buffer = data
        except socket.error, (errno, string):
            self._logger.info("Error at receiving a message")


if __name__ == "__main__":
    ni = NetworkInterface("localhost", 50007)
    ni.sendMessage("Hallo!\n")
    print ni.receiveMessage()
