import unittest
from rsg import CFG


class CFGTest(unittest.TestCase):

    def test_empty_str(self):
    	g = CFG()
    	self.assertEqual(str(g),"")

	


   


if __name__ == "__main__":
	unittest.main()

