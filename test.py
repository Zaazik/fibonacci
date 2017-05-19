import unittest

from fibonacci import Fibonacci



class TestFibonacciMethods(unittest.TestCase):
    def setUp(self):
        self.TEST_CASE = [10, -10, 10.1, -10.1, '10', '-10', '10.1', '-10.1', ]
        self.ERROR_TEST_CASE = ['str', '10.24e']
        self.GOLDEN_DATA = [(0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (5, 5), (6, 8), (7, 13), (8, 21), (9, 34), (10, 55)]

    def test_fibonacci(self):
        for case in self.TEST_CASE:
            f = Fibonacci(case)
            self.assertEqual(f.fibonacci_list, self.GOLDEN_DATA)

        for case in self.ERROR_TEST_CASE:
            with self.assertRaises(Exception) as context:
                Fibonacci(case)
            self.assertTrue('Write correct element number, NOT STRING' in str(context.exception))


if __name__ == '__main__':
    unittest.main()