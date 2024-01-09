import unittest

from in_memory_db import InMemoryDB

class TestInMemoryDBLevel2(unittest.TestCase):
    def setUp(self):
        self.db = InMemoryDB()  # Assuming InMemoryDB is the class you need to test

    def test_scan(self):
        # Assuming 'SET' operation has been tested in Level 1 tests
        self.db.execute(['SET', 0, 'key1', 'A', '1'])
        self.db.execute(['SET', 1, 'key1', 'B', '2'])
        self.db.execute(['SET', 2, 'key1', 'C', '3'])
        scan_result = self.db.execute(['SCAN', 3, 'key1'])
        self.assertEqual(scan_result, "A(1),B(2),C(3)")

    def test_scan_by_prefix(self):
        self.db.execute(['SET', 0, 'key2', 'AA', '1'])
        self.db.execute(['SET', 1, 'key2', 'AB', '2'])
        self.db.execute(['SET', 2, 'key2', 'BA', '3'])
        scan_by_prefix_result = self.db.execute(['SCAN_BY_PREFIX', 3, 'key2', 'A'])
        self.assertEqual(scan_by_prefix_result, "AA(1),AB(2)")

    def test_scan_empty(self):
        scan_empty_result = self.db.execute(['SCAN', 4, 'key3'])
        self.assertEqual(scan_empty_result, "")

    def test_scan_by_prefix_empty(self):
        scan_by_prefix_empty_result = self.db.execute(['SCAN_BY_PREFIX', 5, 'key3', 'Z'])
        self.assertEqual(scan_by_prefix_empty_result, "")

    def test_execute_sequence_level2(self):
        # Sequence of operations including Level 2 operations
        results = self.db.execute_sequence([
            ['SET', 0, 'A', 'BC', '4'],
            ['SET', 10, 'A', 'BD', '5'],
            ['SET', 20, 'A', 'C', '6'],
            ['SCAN_BY_PREFIX', 30, 'A', 'B'],
            ['SCAN', 40, 'A'],
            ['SCAN_BY_PREFIX', 50, 'B', 'B'],
        ])
        self.assertEqual(results, ["", "", "", "BC(4),BD(5)", "BC(4),BD(5),C(6)", ""])

if __name__ == '__main__':
    unittest.main()
