import unittest

from controller import Bulb

class ControllerTests(unittest.TestCase):

    def testBulb_UpdateColor(self):
        b = Bulb('127.0.0.1', 5577)

        # Trigger a failure by passing a length 2 tuple for color
        # color should be a 3 element tuple
        with self.assertRaises(AssertionError) as ae:
            b.update_color((1, 1))
