import unittest
from .. import main
import math

soma = math.pow(2,2)
print(soma)

class MainTestcase(unittest.TestCase):
    def test_restart(self):
        main.vidas = 100
        main.restart()
        self.assertEqual(main.vidas, 3)


if __name__ == '__main__':
    unittest.main()