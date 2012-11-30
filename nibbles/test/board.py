import board
import unittest

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = board.Board(6,6)

    def test_setToken(self):
        self.board.setToken('x',2,2)
        self.assertTrue(self.board._field[2][2] == 'x')

    def test_getToken(self):
        self.board.setToken('y',3,3)
        self.assertTrue(self.board.getToken(3,3) == 'y')

    def test_moveToken(self):
        self.board.setToken('z',1,4)
        self.board.moveToken(1,4,2,4)
        self.assertTrue(self.board.getToken(2,4) == 'z')

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBoard))
    return suite

if __name__ == "__main__":
    unittest.main()
