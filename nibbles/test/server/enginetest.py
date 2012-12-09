# -*- coding: utf-8 *-*

import time
import unittest
import logging
from nibbles.server.engine import *


class CMPDummy():
    """Dummy logger. Has to be replaced!"""
    def __init__(self):
        self.text = None
        self.logger = NibbleStreamLogger("enginetest.cmpdummy")

    def send(self, nibbleid, board, energy, end=False):
        self.text = "%s;%s;%s;%s" % (nibbleid, board, energy, end)
        self.logger.info(self.text)


class RandomDummy():
    def __init__(self):
        pass

    def randint(self, start, end):
        return 0


class TestEngine(unittest.TestCase):
    def setUp(self):
        self.cmp = CMPDummy()
        self.cmp.logger.setLevel(logging.INFO)
        self.engine = Engine(RandomDummy())
        self.engine.setcmp(self.cmp)
        self.engine._board = Board(1, 1)

    def test_register(self):
        self.engine.register()
        self.assertTrue(self.engine._nibblelist[0].getName() == 'a')
        self.assertTrue(len(self.engine._nibblelist) == 1)

    def test_getnibblebyid(self):
        nibbleid = self.engine.register()
        nibble = self.engine.getnibblebyid(nibbleid)
        self.assertEquals(nibble, self.engine._nibblelist[0])

    def test_killnibble(self):
        nibbleid = self.engine.register()
        nibble = self.engine.getnibblebyid(nibbleid)
        self.engine.killnibble(nibbleid)
        self.assertEquals(nibble.getEnergy(), 0)

    def test_gameplay(self):
        # Init engine
        self.engine._logger.setLevel(logging.DEBUG)
        self.engine.setrounds(2)
        # Get nibbles
        n1 = self.engine.register()
        n1 = self.engine.getnibblebyid(n1)
        n2 = self.engine.register()
        n2 = self.engine.getnibblebyid(n2)
        n3 = self.engine.register()
        n3 = self.engine.getnibblebyid(n3)
        # set start time
        td = datetime.timedelta(0, 3)
        self.engine.setgamestart(datetime.datetime.now() + td)
        # Wait for engine to start the game
        time.sleep(td.total_seconds()+1)
        self.assertEquals(self.engine._status, RUNNING)
        # Set up board for first game
        board = self.engine.getboard()
        board._width = 5
        board._height = 5
        board.settoken("*", 0, 0)
        n1.setPos(2, 2)
        board.settoken(n1, 2, 2)
        n2.setPos(1, 1)
        board.settoken(n2, 1, 1)
        n3.setPos(3, 4)
        board.settoken(n3, 3, 4)

        # First move.
        # nibble a
        self.assertEquals(board.getnibbleview(2, 2),
            "*.....b.....a..........c.")
        self.engine.execturn(n1.getName(), 6)
        self.assertFalse(n1.isAlive())
        self.assertEquals(n2.getEnergy(), 67)
        self.assertEquals(board.getnibbleview(2, 2),
            "*.....b................c.")

        #nibble b
        self.assertTrue(self.engine.execturn(n2.getName(), 6) != -1)
        #self.assertEquals(n2.getEnergy(), 69)
        self.assertEquals(board.getnibbleview(2, 2),
            "b......................c.")
        self.engine.execturn(n3.getName(), 0)

        # Second move.
        #n1 is dead.
        self.assertEquals(self.engine.execturn(n1.getName(), 12), -1)
        self.engine.execturn(n2.getName(), 23)
        #n3 is dead.
        # game ended
        self.assertEquals(self.engine.getgamestatus(), ENDED)

    def test_directionandenergy(self):
        d1 = self.engine._calcdirectionoffset(16)[0]
        self.assertEquals(d1, (-1, 1))
        ec = self.engine._calcenergycosts(d1[0], d1[1])
        self.assertEquals(ec, 3)

        (d1, d2) = self.engine._calcdirectionoffset(4)
        self.assertEquals(d1, (+1, -1))
        self.assertEquals(d2, (+1, -1))
        ec = self.engine._calcenergycosts(d1[0] + d2[0], d1[1] + d2[1])
        self.assertEquals(ec, 7)

        (d1, d2) = self.engine._calcdirectionoffset(21)
        self.assertEquals(d1, (0, +1))
        self.assertEquals(d2, (-1, +1))
        ec = self.engine._calcenergycosts(d1[0] + d2[0], d1[1] + d2[1])
        self.assertEquals(ec, 6)

    def test_fight(self):
        aid = self.engine.register()
        did = self.engine.register()
        a = self.engine.getnibblebyid(aid)
        d = self.engine.getnibblebyid(did)

        a.setEnergy(35)
        d.setEnergy(40)
        self.engine._fight(a, d)
        self.assertFalse(a.isAlive())
        self.assertTrue(d.isAlive())

        a.setEnergy(35)
        d.setEnergy(35)
        self.engine._fight(a, d)
        self.assertTrue(a.isAlive())
        self.assertFalse(d.isAlive())

        a.setEnergy(35)
        d.setEnergy(30)
        self.engine._fight(a, d)
        self.assertTrue(a.isAlive())
        self.assertFalse(d.isAlive())
