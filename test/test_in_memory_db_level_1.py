import unittest

from in_memory_db import InMemoryDB

class TestInMemoryDB(unittest.TestCase):
    def setUp(self):
        self.db = InMemoryDB()  # Assuming InMemoryDB is the class you need to test

    def test_set(self):
        self.assertEqual(self.db.execute(['SET', 1, 'key1', 'field1', 'value1']), "")
        self.assertEqual(self.db.execute(['GET', 2, 'key1', 'field1']), 'value1')

    def test_compare_and_set(self):
        self.db.execute(['SET',1, 'key2', 'field2', 'value2'])
        self.assertEqual(self.db.execute(['COMPARE_AND_SET', 2, 'key2', 'field2', 'value2', 'new_value']), "true")
        self.assertEqual(self.db.execute(['GET', 3, 'key2', 'field2']), 'new_value')
        self.assertEqual(self.db.execute(['COMPARE_AND_SET', 4, 'key2', 'field2', 'wrong_value', 'new_value2']), "false")

    def test_compare_and_delete(self):
        self.db.execute(['SET', 1, 'key3', 'field3', 'value3'])
        self.assertEqual(self.db.execute(['COMPARE_AND_DELETE', 2, 'key3', 'field3', 'value3']), "true")
        self.assertEqual(self.db.execute(['GET', 3, 'key3', 'field3']), "")
        self.assertEqual(self.db.execute(['COMPARE_AND_DELETE', 4, 'key3', 'field3', 'value3']), "false")

    def test_get(self):
        self.db.execute(['SET', 1, 'key4', 'field4', 'value4'])
        self.assertEqual(self.db.execute(['GET', 2, 'key4', 'field4']), 'value4')
        self.assertEqual(self.db.execute(['GET', 3, 'key4', 'field_nonexistent']), "")

    def test_execute_sequence(self):
        results = self.db.execute_sequence([
            ['SET', 0, 'A', 'B', '4'],
            ['SET', 1, 'A', 'C', '6'],
            ['COMPARE_AND_SET', 2, 'A', 'B', '4', '9'],
            ['COMPARE_AND_SET', 3, 'A', 'C', '4', '9'],
            ['COMPARE_AND_DELETE', 4, 'A', 'C', '6'],
            ['GET', 5, 'A', 'C'],
            ['GET', 6, 'A', 'B'],
        ])
        self.assertEqual(results, ["","","true","false","true","","9"])

if __name__ == '__main__':
    unittest.main()
