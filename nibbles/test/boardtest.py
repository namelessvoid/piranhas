import unittest

from nibbles.board import *
from nibbles.nibble import *


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board(8, 5)
        self.board.settoken(Nibble("A", 29), 1, 1)
        self.board.settoken(Nibble("B", 30), 0, 0)
        self.board.settoken(Nibble("C", 35), 3, 3)
        self.board.settoken(Nibble("D", 31), 1, 4)
        self.board.settoken("E", 7, 4)
        self.board.settoken("F", 6, 1)
        self.board._logger.setLevel(logging.WARNING)

    def test_gettoken(self):
        self.assertEqual("A", self.board.gettoken(1, 1).getName())
        self.assertEqual("B", self.board.gettoken(0, 0).getName())
        self.assertEqual("C", self.board.gettoken(3, 3).getName())
        self.assertEqual("D", self.board.gettoken(1, 4).getName())

    def test_move(self):
        self.board.move(1, 1, 3, 0)
        self.assertEqual("A", self.board.gettoken(4, 1).getName())
        self.board.move(4, 1, -1, 1)
        self.assertEqual("A", self.board.gettoken(3, 2).getName())
        self.board.move(3, 2, 7, 1)
        self.assertEqual("A", self.board.gettoken(2, 3).getName())

    def test_movetoken(self):
        self.board.movetoken(0, 0, 5, 2)
        self.assertEqual("B", self.board.gettoken(5, 2).getName())
        self.board.movetoken(5, 2, 10, 2)
        self.assertEqual("B", self.board.gettoken(2, 2).getName())

    def test_getter(self):
        self.assertEqual(8, self.board.getwidth())
        self.assertEqual(5, self.board.getheight())

    def test_emptyposition(self):
        self.assertTrue(self.board.emptyposition(7, 2))
        self.assertTrue(self.board.emptyposition(2, 2))

    def test_calcposition(self):
        self.assertEqual((3, 4), self.board.calcposition(3, 4))
        self.assertEqual((4, 2), self.board.calcposition(12, 7))

    def test_tostring(self):
        boardstr = self.board.tostring()
        self.assertEqual("B........A....F............C.....D.....E", boardstr)

    def test_getnibbleview(self):
        nibble = Nibble('X', 30)
        nibble.setPos(7, 4)
        boardview = self.board.getnibbleview(nibble, False)
        self.assertEqual("............E.D...B..F..A", boardview)
        boardview = self.board.getnibbleview(nibble, True)
        self.assertEqual("............E.>...=..F..<", boardview)

    def test_fromstring(self):
        boardstring = self.board.tostring()
        self.board.fromstring(boardstring, 8)
        self.assertEqual(boardstring, self.board.tostring())

        self.assertEqual(self.board.fromstring(boardstring, 7), -1)
