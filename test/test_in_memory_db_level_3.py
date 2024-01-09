import unittest
from in_memory_db import InMemoryDB

class TestInMemoryDBLevel3(unittest.TestCase):
    def setUp(self):
        self.db = InMemoryDB()  # Assuming InMemoryDB is the class you need to test

    def test_set_with_ttl(self):
        self.assertEqual(self.db.execute(['SET_WITH_TTL', 0, 'key1', 'A', '1', '5']), "")
        self.assertEqual(self.db.execute(['GET', 3, 'key1', 'A']), '1')
        self.assertEqual(self.db.execute(['GET', 6, 'key1', 'A']), "")  # TTL expired

    def test_compare_and_set_with_ttl(self):
        self.db.execute(['SET_WITH_TTL', 0, 'key2', 'B', '2', '10'])
        self.assertEqual(self.db.execute(['COMPARE_AND_SET_WITH_TTL', 5, 'key2', 'B', '2', 'new_value', '10']), "true")
        self.assertEqual(self.db.execute(['GET', 15, 'key2', 'B']), "")  # TTL expired after the update

    def test_scan_with_ttl(self):
        self.db.execute(['SET_WITH_TTL', 0, 'key3', 'C', '3', '5'])
        self.db.execute(['SET_WITH_TTL', 1, 'key3', 'D', '4', '10'])
        scan_result_before_ttl = self.db.execute(['SCAN', 2, 'key3'])
        self.assertEqual(scan_result_before_ttl, "C(3),D(4)")
        scan_result_after_ttl = self.db.execute(['SCAN', 12, 'key3'])
        self.assertEqual(scan_result_after_ttl, "")  # All TTL expired

    def test_execute_sequence_level3(self):
        # Sequence of operations including Level 3 operations with TTL
        results = self.db.execute_sequence([
            ['SET', 1, 'A', 'B', '4'],
            ['SET_WITH_TTL', 2, 'X', 'I', '5', '15'],
            ['SET_WITH_TTL', 4, 'A', 'D', '3', '6'],
            ['COMPARE_AND_SET_WITH_TTL', 6, 'A', 'D', '3', '5', '10'],
            ['GET', 7, 'A', 'D'],
            ['SCAN', 15, 'A'],
            ['SCAN', 17, 'A'],
        ])
        self.assertEqual(results, ["", "", "", "true", "5", "B(4),D(5)", "B(4)"])

if __name__ == '__main__':
    unittest.main()
