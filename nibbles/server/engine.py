# import circular list here. -.-
import string
import threading
import datetime
import logging
from nibbles.nibblelogger import NibbleStreamLogger
from nibbles.circularlist import *
from nibbles.nibble import *
from nibbles.board import *
from nibbles.server.serverexceptions import *


""" Engine stats:
        INIT = 0
        RUNNING = 1
        ENDED = 2"""
INIT = 0
RUNNING = 1
ENDED = 2


class Engine():
    def __init__(self, randobj):
        """Initialize the engine.
            Arguments:
                random -- object which proviedes a randint method that
                clones bahaviour of random.randint(...)"""
        # create logger
        self._logger = NibbleStreamLogger("server.engine")
        self._logger.setLevel(logging.DEBUG)

        # Initializes the engine.
        self._nibblelist = CircularList()
        # Create a list which holds all nibble ids.
        self._idlist = string.ascii_letters
        #self._idlist = map(chr, range(ord('a'), ord('z') + 1))
        #self._idlist += map(chr, range(ord('A'), ord('Z') + 1))

        self._nibblestartenergy = 35
        self._fieldspernibble = 3
        self._foodpernibble = 1
        self._energyperfood = 5
        self._turntimeout = 5
        self._status = INIT
        self._currentnibbleid = None
        self._currentround = 0
        self._starttimer = None
        self._energycostlist = [1, 2, 5, 2, 3, 6, 5, 6, 7]
        self._rounds = 10
        self._boardsaves = []

        # Create the board
        self._board = None
        # Create CMPDummy. Hsa to be replaced!
        self._cmp = None
        # Set the random object
        self._random = randobj
        # Lock object
        self._lock = threading.RLock()
        # Update signal
        self.updatesignal = EngineSignal()

    def register(self):
        """Registeres a new nibble.
            Return:
                The id (char) of new nibble.
            Raises:
                RegisterNibbleFailedException"""
      #  with self._lock:
       #     print "Hallo!"

        self._lock.acquire()
        if len(self._nibblelist) == len(self._idlist):
            raise RegisterNibbleFailedException("No more IDs left."
                        + "Cannot register more nibbles!")

        if self._status == RUNNING:
            raise RegisterNibbleFailedException("Game is running."
                        + " Registration disabled.")

        nibbleid = self._idlist[len(self._nibblelist)]
        nibble = Nibble(nibbleid, self._nibblestartenergy)
        self._nibblelist.append(nibble)
        self._logger.info(("Register new nibble with ID '%s' at "
                    + "nibblelist pos %d") % (nibbleid, len(self._nibblelist)))
        self._lock.release()
        return nibbleid

    def killnibble(self, nibbleid):
        """Kills a nibble (set energy to zero) and remove it from the board.
            Argument:
                nibbleid -- (char) The id of the nibble to kill.
            Raises:
                NoSuchNibbleIDException"""
        nibble = None
        try:
            nibble = self.getnibblebyid(nibbleid)
        except NoSuchNibbleIDException, e:
            raise e
        else:
            self._logger.debug("Killing nibble '%s'" % nibbleid)
            nibble._energy = 0
            self._board.settoken(".", nibble._xpos, nibble._ypos)
            # if the current nibble was killed advance with next nibble
#            if self._nibblelist.current() == nibble:
#                self._currentnibbleid = self._nibblelist.next().getName()

    def getnibblebyid(self, nibbleid):
        """Returns a reference to the nibble with nibbleid.
            Arguments:
                nibbleid -- (char) The id of the nibble.
            Return:
                Reference to the nibble.
            Raises:
                NoSuchNibbleIDException"""
        searchednibble = None
        for nibble in self._nibblelist:
            if nibble.getName() == nibbleid:
                searchednibble = nibble
                break
        if not searchednibble:
            msg = "No such nibble with ID %s" % (nibbleid)
            self._logger.WARNING(msg)
            raise NoSuchNibbleIDException(msg)
        else:
            return searchednibble

    def getcurrentnibbleid(self):
        """Get the current nibble.
            Return:
                Reference to the nibble. None if the game is not running."""
        if self._status != RUNNING:
            return None
        else:
            return self.getnibblebyid(self._currentnibbleid)._NAME

    def getgamestatus(self):
        """Get the status of the game.
            Return: INIT, RUNNING or ENDED"""
        return self._status

    def setfoodpernibble(self, number):
        """Sets the amount of food to be dropped per nibble each round.
            Arguments:
                number --  (integer) the amount of the food."""
        self._foodpernibble = number

    def setfieldspernibble(self, number):
        """Sets the number of fields to be added to the board per nibble.
            Arguments:
                number -- (integer) the number of fields
                (both, x and y directoin)"""
        self._fieldspernibble = number

    def setrounds(self, number):
        """Sets the number of rounds the game should last.
            Arguments:
                number -- (integer) the number of rounds"""
        self._rounds = number

    def setturntimeout(self, seconds):
        """Sets the timeout of one turn in seconds. When it's nibble X's turn
            and X does not move within the given period, the engine assumes
            that X does not want to move and continues.
            Arguments:
                seconds -- (integer) the timeout as integer"""
        self._turntimeout = seconds

    def setcmp(self, cmp):
        """Sets the command processor of the engine.
            Arguments:
                cmp -- (CommandProcessor) The CMP to use. Can also be a dummy
                       Which implements the behaviour of the cmp that is
                       called by the engine."""
        self._cmp = cmp

    def getboard(self):
        """Get the board.
            Return:
                board -- (Board) The instance of board that is used
                         in the engine."""
        return self._board

    def setgamestart(self, date):
        """Sets the time when the game begins and executes the timer which
            calls self.run() when the game begins.
            Arguments:
                date -- (datetime.datetime) the time"""
        self._gamestart = date
        now = datetime.datetime.now()
        waittime = (date - now).total_seconds()
        self._logger.debug("Set start time to: %s (%d seconds)"
                % (date, waittime))
        self._timer = threading.Timer(waittime, self._startgame)
        self._timer.start()

    def _startgame(self):
        """Starts the game"""
        self._logger.info("Game started (gamestart: %s)" % self._gamestart)
        # Create board
        boardsize = self._fieldspernibble * len(self._nibblelist)
        self._board = Board(boardsize, boardsize)
        # set first round
        self._currentround = 1

        # Place nibbles randomly on the board TODO
        for n in self._nibblelist:
            x, y = 0, 0
            while True:
                x = self._random.randint(0, self._board.getwidth())
                y = self._random.randint(0, self._board.getheight())
                if self._board.gettoken(x, y) == '.':
                    break
            self._board.settoken(n, x, y)
            n.setPos(x, y)
            self._logger.debug(("Placed nibble at n.(%s/%s)."
                + " Content of board: %s") % (n._xpos, n._ypos,
                self._board.gettoken(n._xpos, n._ypos).getName()))

        # Signal changes
        self.updatesignal.call()
        # Set first player
        self._currentnibbleid = self._nibblelist.current().getName()
        # Set status to running
        self._timer = threading.Timer(self._turntimeout, self.execturn,
            args=[self._currentnibbleid, 12])
        self._timer.start()
        # send board information to first nibble
        self._saveboard()
        self._sendtocmp()
        self._logger.debug("Game start succesfull.")
        self._logger.info("Began round %i of %i"
            % (self._currentround, self._rounds))
        self._status = RUNNING

    def execturn(self, nibbleid, direction):
        """Moves a nibble aka execute one game turn:
            0.) Interrupt playertimeout timer
            1.) Get the direction in which current nibble moves.
            2.) Use up energy for move
            3.) Combat / Food consumption
            4.) Move the nibble on the actual board
            5.) Set new current nibble

            TODO: Multiple combat"""

        self._logger.debug(("Try to execute turn of '%c' in round %i." +
            " Current nibble is '%c'")
            % (nibbleid, self._currentround, self._currentnibbleid))
        self._logger.debug("Full board in turn %i: %s"
            % (self._currentround, self._board.tostring()))

        # Wrong player wanted to move
        if not nibbleid == self._currentnibbleid:
            return -1
        if not self._status == RUNNING:
            self._logger.info("Cannot execute turn. Game not running!")
            return -1

        nibble = self.getnibblebyid(self._currentnibbleid)

        # 0.) Interrupt timer
        self._timer.cancel()

        # 1.) direction
        deltas = self._calcdirectionoffset(direction)
        for (dx, dy) in deltas:
            self._nibblestep(nibble, dx, dy)

        #Use up energy for move
        energycosts = self._calcenergycosts(direction)
        nibble.setEnergy(nibble.getEnergy() - energycosts)

        # 5.) set next player
        self._nextnibble()
        self.updatesignal.call()
        return 0

    def _nibblestep(self, nibble, dx, dy):
        """Moves the nibble one step wide. This is needed if the nibble does a
            knight like chess move.
            Arguments:
                nibble -- (Nibble) The current moving nibble
                dx, dy -- (int) The directino offsets calculated
                          by engine._calcdirectionoffset()."""

        #todo: nibble alive?
        (oldx, oldy) = nibble.getPos()
        newx = oldx + dx
        newy = oldy + dy

        #combat / food consumption
        token = self._board.gettoken(newx, newy)
        if token in self._nibblelist and token != nibble:
            self._fight(nibble, token)
        elif token == "*":
            nibble.setEnergy(nibble.getEnergy() + self._energyperfood)

        # if not killed, move the nibble
        if nibble.isAlive():
            self._board.movetoken(oldx, oldy, newx, newy)
            nibble.setPos(newx, newy)
        # if killed, remove nibble from the board
        else:
            self._board.settoken('.', oldx, oldy)

    def _endgame(self):
        """"""
        self._logger.info("Game ended in round '%i' of '%i'"
            % (self._currentround, self._rounds))
        self._status = ENDED
        # Send past 10 boards to clients
        for nibble in self._nibblelist:
            for board in self._boardsaves:
                self._cmp.send(nibble.getName(), board, 0, True)
        self.updatesignal.call()

    def _calcdirectionoffset(self, number):
        """Takes a direction number between 0 and 24 to calculate the x and
            y offsets of the given direction.
            Argument:
                number - (int) between 0 and 24 which describes the direction.
            Return:
                ((dx1, dy1), (dx2, dy2) -- touple of two int tuples which hold
                the realtive x and y offsets to perform the move. If only one
                step is needed to perform this step, the second touple is None.
            Raises:
                ValueError"""
        if not 0 <= number <= 24:
            msg = (("No such direction description: %d. Must "
                  + "be between 0 and 24!") % number)
            self._logger.warning(msg)
            raise ValueError(msg)

        (x, y) = (number % 5 - 2, number / 5 - 2)

        # break up double steps into single steps
        # if it's just a single step
        if max(abs(x), abs(y)) == 1:
            return((x, y),)
        # 'knight' like step
        elif abs(x * y) == 2:
            if abs(x) == 2:
                return ((x / 2, 0), (x / 2, y))
            else:
                return ((0, y / 2), (x, y / 2))
        # double step to the corners or in one direction
        else:
            return ((x / 2, y / 2), (x / 2, y / 2))

    def _calcenergycosts(self, number):
        """Calculate the energy that the nibble has to spend to move to the
            field given by dx and dy.
            Argument:
                number - (int) between 0 and 24 which describes the direction.
            Return:
                energycosts -- (int) the energy costs as interger"""

        if not 0 <= number <= 24:
            msg = (("No such direction description: %d. Must "
                  + "be between 0 and 24!") % number)
            self._logger.warning(msg)
            raise ValueError(msg)

        (x, y) = (number % 5 - 2, number / 5 - 2)
        x = abs(x)
        y = abs(y)
        return self._energycostlist[y + x * 3]

    def _fight(self, attacker, defender):
        """Simulates the fight between two nibbles. Kills the nibble
            that looses the fight and calculate energy for the winner.
            Arguments:
                attacker -- (nibble) the attacking nibble
                defender -- (nibble) the defending nibble"""
        self._logger.debug("Nibble fight: attacker %s vs. %s defender" %
                (attacker.getName(), defender.getName()))

        if defender.getEnergy() > attacker.getEnergy():
            self._logger.debug("Nibble fight: Winner is defender %s." %
                    defender.getName())
            defender.setEnergy(defender.getEnergy() + attacker.getEnergy())
            self.killnibble(attacker.getName())

        else:
            self._logger.debug("Nibble fight: Winner is attacker %s." %
                    attacker.getName())
            attacker.setEnergy(defender.getEnergy() + attacker.getEnergy())
            self.killnibble(defender.getName())

    def _dropfood(self):
        """Place food on the baord randomly. The amount of food dropped is
            the number of nibbles * self._foodpernibble. If food drops on a
            nibble the lucky one can eat at once."""
        for i in range(self._foodpernibble * len(self._nibblelist)):
            rx = self._random.randint(0, self._board._width - 1)
            ry = self._random.randint(0, self._board._height - 1)
            # if a nibble is on the chosen location, feed it
            token = self._board.gettoken(rx, ry)
            if isinstance(token, Nibble):
                token.setEnergy(token.getEnergy() + self._energyperfood)
            else:
                self._board.settoken("*", rx, ry)

    def _nextnibble(self):
        """Sets the next nibble and restarts the timer."""
        self._logger.debug("_nextnibble: current nibble '%c'" %
            self._currentnibbleid)
        while 1:
            nibble = self._nibblelist.next()

            # if first nibble is reached, one turn has passed
            if(self._nibblelist[0] == nibble):
                self._saveboard()
                # if this was the last round stop the game
                if self._currentround >= self._rounds:
                    self._endgame()
                    return

                self._currentround += 1
                self._logger.info("Began round %i of %i."
                    % (self._currentround, self._rounds))
                self._dropfood()

            # if nibble is dead, continue with loop
            if not nibble.isAlive():
                self._logger.debug("in _nextnibble(): found dead nibble."
                    + " Continuing...")
                self._currentnibbleid = nibble.getName()
                self._sendtocmp()
            else:
                break

        self._logger.debug("_nextnibble: previous nibble '%c', new nibble '%c'"
            % (self._currentnibbleid, nibble.getName()))

        self._currentnibbleid = nibble.getName()
        self._timer = threading.Timer(self._turntimeout, self.execturn,
            args=[self._currentnibbleid, 12])
        self._timer.start()
        self._logger.debug("Restartet turn timeout timer.")
        self._sendtocmp()

    def _sendtocmp(self):
        """Sends a message to the cmp which holds nibbleid,
            the part of the board that's visible to the nibble
            and its energy."""
        nibble = self.getnibblebyid(self._currentnibbleid)
        energy = 0
        boardview = ""
        if nibble.isAlive():
            energy = nibble.getEnergy()
            (x, y) = nibble.getPos()
            boardview = self._board.getnibbleview(nibble, True)
        self._logger.debug("Sending %s, %s, %s to cmp."
            % (self._currentnibbleid, boardview, energy))
        self._cmp.send(self._currentnibbleid, boardview, energy)

    def _saveboard(self):
        """Saves the board of the current turn and holdas up to 10 saves."""
        # If already 10 boards were saved, remove the oldest one.
        if len(self._boardsaves) == 10:
            self._boardsaves.pop(0)
        self._boardsaves.append(self._board.tostring())


class EngineSignal(object):
    """Simple signal which calls a number of saved functions."""
    def __init__(self):
        self.listeners = []

    def register(self, function):
        """Register a function to the signal.
            Arguments:
                function --- (function object) the function to be registered"""
        self.listeners.append(function)

    def remove(self, function):
        """Removes the gifen function from the signal.
            Arguments:
                function -- (function object) the function to be removed"""
        self.listeners.remove(function)

    def call(self):
        """Calls all function safed in the signal."""
        for f in self.listeners:
            f()
