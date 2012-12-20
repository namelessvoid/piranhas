import logging
import threading

from nibbles.nibblesignal import NibbleStringSignal

class NibbleLogger(object):
    def __init__(self, logger="default.default", level=logging.DEBUG):
        self._logger = logging.getLogger(logger)
        self._logger.setLevel(level)
        self._formatter = logging.Formatter("%(asctime)s %(levelname)s: %(name)s: %(message)s", "%d.%m.%Y %H:%M:%S")
        self.setFormatter(self._formatter)
        self._logger.addHandler(self)
        self.logsignal = NibbleStringSignal()
        qthandler = QtHandler(self.logsignal, level)
        qthandler.setFormatter(self._formatter)
        self._logger.addHandler(qthandler)

    def log(self, level, message):
        self._logger.log(level, message)

    def debug(self, message):
        self._logger.debug(message)

    def info(self, message):
        self._logger.info(message)

    def error(self, message):
        self._logger.error(message)

    def warning(self, message):
        self._logger.warning(message)

    def critical(self, message):
        self._logger.critical(message)


class NibbleStreamLogger(logging.StreamHandler, NibbleLogger):
    def __init__(self, logger="default.default", level=logging.DEBUG, stream=None):
        logging.StreamHandler.__init__(self, stream)
        NibbleLogger.__init__(self, logger, level)


class NibbleFileLogger(logging.FileHandler, NibbleLogger):
    def __init__(self, logger="default.default", level=logging.DEBUG, filename="testlog.txt", filemode="a"):
        logging.FileHandler.__init__(self, filename, filemode)
        NibbleLogger.__init__(self, logger, level)


class QtHandler(logging.Handler):
    """A custom implementation of handler that handles the
        logging for Qt guis."""
    def __init__(self, logsignal, level=logging.DEBUG):
        """Constructor of QtHandler.
            Arguments:
                logsignal -- (nibbles.nibblesignal.NibbleStringSignal) the
                             signal that is emitted when something is logged.
                level    --  (logging.LEVEL) a loglevel specified in the
                             python logging framework."""
        super(QtHandler, self).__init__(level)
        self._logsignal = logsignal

    def handle(self, record):
        """Overwrite the logging.Handler.handle() method. This method
            just emits the logsignal that is processes within the gui.
            Arguments:
                record -- (logging.record) record file of pythons logging
                          framework"""
        msg = self.format(record)
        self._logsignal.callstr(msg)
