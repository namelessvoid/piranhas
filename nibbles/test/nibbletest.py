# -*- coding: utf-8 *-*

import unittest

from nibbles.nibble import *


class TestNibble(unittest.TestCase):

    def setUp(self):
        self.nibble = Nibble('O', 30)

    def test_getEnergy(self):
        self.assertTrue(self.nibble.getEnergy() == 30)

    def test_setEnergy(self):
        self.nibble.setEnergy(25)
        self.assertTrue(self.nibble.getEnergy() == 25)

    def test_isAlive(self):
        self.nibble.setEnergy(5)
        self.assertTrue(self.nibble.isAlive())
        self.nibble.setEnergy(0)
        self.assertFalse(self.nibble.isAlive())

    def test_getName(self):
        self.assertTrue(self.nibble.getName() == 'O')

    def test_getPos(self):
        x, y = self.nibble.getPos()
        self.assertTrue(x == -1 and y == -1)

    def test_setPos(self):
        self.nibble.setPos(2, 3)
        x, y = self.nibble.getPos()
        self.assertTrue(x == 2 and y == 3)
