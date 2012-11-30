# -*- coding: utf-8 *-*

#from exceptions import *


class RegisterNibbleFailedException(Exception):
    def __init__(self, msg):
        self.msg = msg


class NoSuchNibbleIDException(BaseException):
    def __init__(self, msg):
        self.msg = msg
