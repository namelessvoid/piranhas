import logging

class NibbleLogger(object):
    def __init__(self, logger="default.default", level=logging.DEBUG):
        self._logger = logging.getLogger(logger)
        self._logger.setLevel(level)
        self._formatter = logging.Formatter("%(asctime)s %(levelname)s: %(name)s: %(message)s", "%d.%m.%Y %H:%M:%S")
        self.setFormatter(self._formatter)
        self._logger.addHandler(self)

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

class NibbleQTextEditLogger(logging.Handler, NibbleLogger):
    def __init__(self, text_edit, logger="default.default", level=logging.DEBUG):
        logging.Handler.__init__(self)
        NibbleLogger.__init__(self, logger, level)
        self.text_edit = text_edit

    def emit(self, record):
        self.text_edit.append(self.format(record))

if __name__ == "__main__":
    my_logger = NibbleStreamLogger()
    my_logger.info("Testnachricht")
    my_logger.warning("Testnachricht")
    my_logger.critical("Testnachricht")
    my_logger.error("Testnachricht")
    my_logger.log(logging.ERROR, "Testnachricht")

    #my_logger2 = NibbleFileLogger()
    #my_logger2.info("Testnachricht von FileLogger")


