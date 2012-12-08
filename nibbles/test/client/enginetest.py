import sys
from StringIO import StringIO
import unittest
sys.path.insert(0, "../../")
from nibbles.client.engine import *

class TestEngine(unittest.TestCase):

    def setUp(self):
        self._engine = Engine()
        self.held, sys.stdout = sys.stdout, StringIO()

    def test_run(self):
        self.assertRegexpMatches("23x14@", "\d+x\d+@")
        self.assertRegexpMatches("2012-11-17 00:00:00@", "\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2}@")
        self._engine.run()
        self.assertEqual(sys.stdout.getvalue(),"2012-11-17 00:00:00@")

    def test_printMessage(self):
        self._engine.printmessage("message")
        self.assertEqual(sys.stdout.getvalue(),"message")
