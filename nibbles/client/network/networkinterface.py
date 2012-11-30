""" The client's network interface.

    The network interface takes strings from the engine and sends them to the
    socket which esatblished the connection to the server.
    Also it receives messages from the server and hands them over to the
    engine."""

import socket
import logging


class NetworkInterface(socket.socket):
    #_s, _host, _port = (None, None, None)

    def __init__(self, host, port):
        """Initialize the NetworkInterface
        host:    string that holds the address of the host
        port:    integer that holds the destination port"""
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM)
        self._host = host
        self._port = port
        self.connect((self._host, self._port))
        logging.info("NetworkInterface connected to %s:%d" % (host, port))

    def sendmessage(self, message):
        """Sends a message to the host.
        message: string representation of the message."""
        logging.info("NetworkInterface.sendMessage(\"" + message + "\")")
        socketfile = self.makefile()
        socketfile.write(message)
        logging.info("NetworkInterface.sendMessage() DONE")
        socketfile.close()

    def receivemessage(self):
        """Receives a message from the host.
        return value: String which holds the message"""
        logging.info("NetworkInterface().receiveMessage()")
        message = ""
        self.setblocking(0)
        try:
            while 1:
                data = self.recv(1024)
                if not data:
                    break
                logging.info("received: " + str(data))
                message += data
        except socket.error, (errno, string):
            if errno == 11:
                return message
            else:
                print str(errno) + string
        finally:
            self.setblocking(1)
        return message

if __name__ == "__main__":
    ni = NetworkInterface("localhost", 50007)
    ni.sendMessage("Hallo!\n")
    print ni.receiveMessage()
