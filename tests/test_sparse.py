import unittest
from raresim.common.sparse import SparseMatrix

class TestSparseMatrix(unittest.TestCase):
    def setUp(self):
        # Initialize a 3x5 sparse matrix (3 rows, 5 columns)
        self.matrix = SparseMatrix(cols=5)
        # Add rows first
        for _ in range(3):
            self.matrix.add_row([])
        # Now add values
        self.matrix.add(0, 1)
        self.matrix.add(0, 3)
        self.matrix.add(1, 2)
        self.matrix.add(2, 0)
        self.matrix.add(2, 4)

    def test_get(self):
        self.assertEqual(self.matrix.get(0, 1), 1)
        self.assertEqual(self.matrix.get(0, 2), 0)
        self.assertEqual(self.matrix.get(2, 4), 1)

    def test_get_row(self):
        self.assertEqual(self.matrix.get_row(0), [0, 1, 0, 1, 0])
        self.assertEqual(self.matrix.get_row(1), [0, 0, 1, 0, 0])
        self.assertEqual(self.matrix.get_row(2), [1, 0, 0, 0, 1])

    def test_add_remove(self):
        # Add a value and test
        self.matrix.add(0, 2)
        self.assertEqual(self.matrix.get(0, 2), 1)
        # Remove the value and test
        self.matrix.remove(0, 2)
        self.assertEqual(self.matrix.get(0, 2), 0)

    def test_num_rows_cols(self):
        self.assertEqual(self.matrix.num_rows(), 3)
        self.assertEqual(self.matrix.num_cols(), 5)

if __name__ == '__main__':
    unittest.main()
