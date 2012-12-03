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
        self._logger.setLevel(logging.WARNING)

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

        # Create the board
        self._board = None
        # Create CMPDummy. Hsa to be replaced!
        self._cmp = None
        # Set the random object
        self._random = randobj

    def register(self):
        """Registeres a new nibble.
            Return:
                The id (char) of new nibble.
            Raises:
                RegisterNibbleFailedException"""
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
        self._logger.info(self._nibblelist)
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
            nibble._energy = 0
            self._board.settoken(".", nibble._xpos, nibble._ypos)
            # if the current nibble was killed advance with next nibble
            if self._nibblelist.current() == nibble:
                self._currentnibbleid = self._nibblelist.next().getName()

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
            raise NoSuchNibbleIDException("No such nibble with ID %s"
                    % (nibbleid))
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
        self._logger.info("Set start time to: %s (%d seconds)"
                % (date, waittime))
        self._timer = threading.Timer(waittime, self._startgame)
        self._timer.start()

    def _startgame(self):
        """Starts the game"""
        # Create board
        boardsize = self._fieldspernibble * len(self._nibblelist)
        self._board = Board(boardsize, boardsize)
        # set first round
        self._currentround = 1

        # Place nibbles randomly on the board TODO
        for n in self._nibblelist:
            x = self._random.randint(0, self._board.getwidth)
            y = self._random.randint(0, self._board.getheight)
            self._board.settoken(n, x, y)
            n.setPos(x, y)

        # Set first player
        self._currentnibbleid = self._nibblelist.current().getName()
        # Set status to running
        self._status = RUNNING
        self._logger.info("Game started (gamestart: %s)" % self._gamestart)
        self._timer = threading.Timer(self._turntimeout, self.execturn,
            args=[self._currentnibbleid, 12])
        # send board information to first nibble
        self._sendtocmp()
        # TODO signal game end to cmp?

    def execturn(self, nibbleid, direction):
        """Moves a nibble aka execute one game turn:
            0.) Interrupt playertimeout timer
            1.) Get the direction in which current nibble moves.
            2.) Use up energy for move
            3.) Combat / Food consumption
            4.) Move the nibble on the actual board
            5.) Check for gameend
            6.) Set new current nibble

            TODO: Multiple combat"""

        # Wrong player wanted to move
        if not nibbleid == self._currentnibbleid:
            return -1

        nibble = self.getnibblebyid(self._currentnibbleid)

        # 0.) Interrupt timer
        self._timer.cancel()

        # 1.) direction
        (dx, dy) = self._calcdirectionoffset(direction)
        (oldx, oldy) = nibble.getPos()
        newx = oldx + dx
        newy = oldy + dy

        # 2.) Use up energy for move
        energycosts = self._calcenergycosts(dx, dy)
        nibble.setEnergy(nibble.getEnergy() - energycosts)

        # 3.) combat / food consumption
        token = self._board.gettoken(newx, newy)
        self._logger.warning(token)
        # enemy found?
        if token in self._nibblelist:
            self._fight(nibble, token)
        # food found?
        elif token == "*":
            nibble.setEnergy(nibble.getEnergy() + self._energyperfood)

        # 4.) move
        # nibble not killed by enemy?
        if nibble.isAlive():
            self._board.movetoken(oldx, oldy, newx, newy)
            nibble.setPos(newx, newy)
        # if nibble was killed, remove it from the board
        else:
            self._board.settoken('.', oldx, oldy)

        # 5.) game end?
        if self._currentround == self._rounds or len(self._nibblelist) <= 1:
            self._endgame()
        # 6.) set next player
        else:
            self._nextnibble()

    def _endgame(self):
        # TODO: Send past 10 boards to clients
        self._status = ENDED

    def _calcdirectionoffset(self, number):
        """Takes a direction number between 0 and 24 to calculate the x and
            y offsets of the given direction.
            Argument:
                number - (int) between 0 and 24 which describes the direction.
            Return:
                (dx, dy) - (int tuple) delta x and delta y
            Raises:
                ValueError"""
        if not 0 <= number <= 24:
            raise ValueError("No such direction description: %d. Must" +
                  + "be between 0 and 24!" % number)
        else:
            return (number % 5 - 2, number / 5 - 2)

    def _calcenergycosts(self, dx, dy):
        """Calculate the energy that the nibble has to spend to move to the
            field given by dx and dy.
            Argument:
                dx -- (int) delta x
                dy -- (int) delta y"""
        dx = abs(dx)
        dy = abs(dy)
        return self._energycostlist[dy + dx * 3]

    def _fight(self, attacker, defender):
        """Simulates the fight between two nibbles. Kills the nibble
            that looses the fight and calculate energy for the winner.
            Arguments:
                attacker -- (nibble) the attacking nibble
                defender -- (nibble) the defending nibble"""
        self._logger.info("Nibble fight: attacker %s vs. %s defender" %
                (attacker.getName(), defender.getName()))

        if defender.getEnergy() > attacker.getEnergy():
            self._logger.info("Nibble fight: Winner is defender %s." %
                    defender.getName())
            defender.setEnergy(defender.getEnergy() + attacker.getEnergy())
            self.killnibble(attacker.getName())

        else:
            self._logger.info("Nibble fight: Winner is attacker %s." %
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
                self._board.settoken("*", ry, ry)

    def _nextnibble(self):
        """Sets the next nibble and restarts the timer."""
        while 1:
            nibble = self._nibblelist.next()
            # nibble is dead
            if not nibble.isAlive():
                self._cmp.send(nibble.getName(), "", "")
            else:
                break

        self._currentnibbleid = nibble.getName()
        self._timer = threading.Timer(self._turntimeout, self.execturn,
            args=[self._currentnibbleid, 12])
        self._sendtocmp()

        # if first nibble is reached, one turn has passed
        if(self._nibblelist[0] == nibble):
            self._currentround += 1
            self._dropfood()

    def _sendtocmp(self):
        """Sends a message to the cmp which holds nibbleid,
            the part of the board that's visible to the nibble
            and its energy."""
        nibble = self.getnibblebyid(self._currentnibbleid)
        boardview = self._board.getnibbleview(nibble._xpos, nibble._ypos)
        self._cmp.send(self._currentnibbleid, boardview, nibble.getEnergy())
