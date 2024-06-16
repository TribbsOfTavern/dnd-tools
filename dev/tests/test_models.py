import sys
import unittest
from unittest.mock import patch, MagicMock

from models import Table, Result, Link, Resolver
import tests.test_dicts as test_tables

class TestTable(unittest.TestCase):
    # test_tables.table_a   # Table is valid
    # test_tables.table_b   # Table is missing 'roll'
    # test_tables.table_c   # Table has an invalid roll
    # test_tables.table_d   # Table is missing table-name
    # test_tables.table_e   # Table has an invalid table-name

    def test_create(self):
        """ Test Table creation. """
        table_a = Table.create(test_tables.table_a)
        table_b = Table.create(test_tables.table_b)
        table_c = Table.create(test_tables.table_c)
        table_d = Table.create(test_tables.table_d)
        table_e = Table.create(test_tables.table_e)
        self.assertIsNotNone(table_a)
        self.assertIsNone(table_b)
        self.assertIsNone(table_c)
        self.assertIsNone(table_d)
        self.assertIsNone(table_e)

    def test_getRawResult(self):
        """ Test raw result retrieval. """
        table = Table.create(test_tables.table_a)

        self.assertEqual(table.getRawResult(1), "Example 1: single inline rolls -> [1d4]")
        self.assertEqual(table.getRawResult(7), "Example 7: there is no link in this example")
        self.assertEqual(table.getRawResult(2), "Example 2: single inline link -> [1@Test Table B]")
        self.assertEqual(table.getRawResult(100), None)
        self.assertEqual(table.getRawResult("foo"), None)

    def test_getResult(self):
        """ Test Result object retrieval. """
        table = Table.create(test_tables.table_a)

        self.assertIsInstance(table.getResult(1), Result)
        self.assertIsInstance(table.getResult(7), Result)
        self.assertIsNone(table.getResult(100))
        self.assertIsNone(table.getResult("Foo"))

    def test_resultExists(self):
        """ Test result exists check """
        table = Table.create(test_tables.table_a)
        res_amount = table.length

        for i in range(1, res_amount+1):
            self.assertTrue(table.resultExists(i))
        self.assertFalse(table.resultExists(100))
        self.assertFalse(table.resultExists("foo"))

    def test_validateTable(self):
        """ Test Table validation """
        table = Table() # Empty class to use validateTable

        self.assertTrue(table.validateTable(test_tables.table_a))
        self.assertFalse(table.validateTable(test_tables.table_b))
        self.assertFalse(table.validateTable(test_tables.table_c))
        self.assertFalse(table.validateTable(test_tables.table_d))
        self.assertFalse(table.validateTable(test_tables.table_e))

class TestResult(unittest.TestCase):    
    def test_createResult(self):
        """ Test creation and initialization of Result object. """
        # Test Creation
        test = Result.create("This is a test -> [1d4] [1@Test Table]")
        self.assertIsNotNone(test)
        # Test Failed Creation
        with self.assertRaises(TypeError):
            Result.create()
        # Test Garbage Creation
        test = Result.create(111)
        self.assertIsNone(test)

    def test_settingText(self):
        """ Test setting Result.text """
        test = Result.create("Foo")
        # Set Result.text to a string
        test.text = "bar"
        self.assertEqual(test.text, "bar")
        # Set Result.text to None
        test.text = None
        self.assertEqual(test.text, "")
        # Set Result.text to int
        test.text = 111
        self.assertEqual(test.text, "")
        # Set result with a new string containing inline links
        test.text = "1 Foobar..."
        self.assertEqual(test.text, "1 Foobar...")
        self.assertIsNone(test.links)          
        test.text = "This contains [1d4] Foobars!"
        self.assertEqual(test.text, "This contains [1d4] Foobars!")
        self.assertIn("1d4", test.links)

class TestLink(unittest.TestCase):
    def test_linkCreation(self):
        ''' Test creation of link. This test also returns the dict which allows
            for the testing of each variable within the Link Obj.'''
        test = Link.create("1d6")
        self.assertDictEqual(test.getDict(), {
            "text": "1d6",
            "type": "roll",
            "roll": "1d6",
            "table": ''
        }, "Link with just roll.")

        test = Link.create("1@Test Table")
        self.assertDictEqual(test.getDict(), {
            "text": "1@Test Table",
            "type": "table",
            "roll": "1",
            "table": "Test Table"
        }, "Link with fixed amount on table..")

        test = Link.create("1d3@Test Table")
        self.assertDictEqual(test.getDict(), {
            "text": "1d3@Test Table",
            "type": "table",
            "roll": "1d3",
            "table": "Test Table"
        }, "Link with roll amount on table.")
        
        test = Link.create("1f6")
        self.assertIsNone(test)

        test = Link.create("a")
        self.assertIsNone(test)

        test = Link.create("1f4@Test")
        self.assertIsNone(test)

        test = Link.create("a@Test")
        self.assertIsNone(test)

        test = Link.create("")
        self.assertIsNone(test)

