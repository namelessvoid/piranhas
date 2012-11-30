# -*- coding: utf-8 *-*
import unittest

from nibbles.circularlist import *


class TestCircularList(unittest.TestCase):

    def setUp(self):
        self.cl = CircularList()

    def test_circular(self):
        self.cl.append(1)
        self.cl.append(2)
        self.cl.append(3)

        self.assertTrue(self.cl.current() == 1)
        for i in range(2):
            self.assertTrue(self.cl.next() == 2)
            self.assertTrue(self.cl.next() == 3)
            self.assertTrue(self.cl.next() == 1)

    def test_empty(self):
        self.assertTrue(self.cl.current() is None)
        self.assertTrue(self.cl.next() is None)
