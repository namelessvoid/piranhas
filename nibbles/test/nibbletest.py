# -*- coding: utf-8 *-*

import unittest

from nibbles.nibble import *


class TestNibble(unittest.TestCase):

    def setUp(self):
        self.nibble = Nibble('O', 30)

    def test_getenergy(self):
        self.assertTrue(self.nibble.getenergy() == 30)

    def test_setenergy(self):
        self.nibble.setenergy(25)
        self.assertTrue(self.nibble.getenergy() == 25)

    def test_isalive(self):
        self.nibble.setenergy(5)
        self.assertTrue(self.nibble.isalive())
        self.nibble.setenergy(0)
        self.assertFalse(self.nibble.isalive())

    def test_getname(self):
        self.assertTrue(self.nibble.getname() == 'O')

    def test_getpos(self):
        x, y = self.nibble.getpos()
        self.assertTrue(x == -1 and y == -1)

    def test_setpos(self):
        self.nibble.setpos(2, 3)
        x, y = self.nibble.getpos()
        self.assertTrue(x == 2 and y == 3)
