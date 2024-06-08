import unittest
from unittest.mock import patch, MagicMock

import random
import dice_utils

class TestDieFuncs(unittest.TestCase):
    def test_isValid(self):
        """ Test Roll Validation """
        test_rolls = [
            "1d6",  "4d6kh3",   "2d20kl1",
            "2d8kh1",   "2d6+2",    "2d6kh1+2",
            "2d100kh1/2",   "2d50kl1*3",    "3d6-4",
            "1f6", "d6", "d",
            "1d+2" 
        ]

        expected_verified = [
            True,   True,   True,
            True,   True,   True,
            True,   True,   True,
            False,  False, False,
            False
        ]

        for i in range(0, len(test_rolls)):
            self.assertEqual(expected_verified[i], dice_utils.is_valid(
                test_rolls[i]))

    @patch('dice_utils.randint')
    def test_parseRolls(self, mock_randint):
        """ Test Parsing Rolls """
        # Normal Roll of 1 D 6
        roll_notation = "1d6"
        mock_randint.return_value = 2
        test = dice_utils.parse_rolls(roll_notation)
        self.assertEqual(test, {"rolls": [2]})
        # Normal Roll of 2 D 20
        roll_notation = "2d20"
        mock_randint.side_effect = [10, 18]
        test = dice_utils.parse_rolls(roll_notation)
        self.assertEqual(test, {"rolls": [10, 18]})
        mock_randint.side_effect = None
        # Incorrect roll notation A: 2 F 20
        roll_notation = "2f20"
        test = dice_utils.parse_rolls(roll_notation)
        self.assertIsNone(test)
        # Negative Dice rolls
        roll_notation = "-2d20"
        test = dice_utils.parse_rolls(roll_notation)
        self.assertIsNone(test)
        # Negative Dice Sides
        roll_notation = "2d-20"
        test = dice_utils.parse_rolls(roll_notation)
        self.assertIsNone(test)
        # Empty Roll Notation
        roll_notation = ""
        test = dice_utils.parse_rolls(roll_notation)
        self.assertIsNone(test)

    def test_parseKeeps(self):
        """ Test Parsing Keep Rolls """
        # Keep Highest 1 of rolls [4]
        test = dice_utils.parse_keeps("1d6kh1", [4])
        self.assertDictEqual(test, {"keep": "kh", "value": 1})
        # Roll [1, 4, 6] keep highest 2
        test = dice_utils.parse_keeps("3d6kh2", [1, 4, 6])
        self.assertDictEqual(test, {"keep": "kh", "value": 2})
        # Roll [1, 4, 6] keep lowest 2
        test = dice_utils.parse_keeps("3d6kl2", [1, 4, 6])
        self.assertDictEqual(test, {"keep": "kl", "value": 2})
        # Roll [1, 4, 6] keep highest 5
        test = dice_utils.parse_keeps("3d6kh5", [1, 4, 6])
        self.assertIsNone(test)
        # Roll [1, 4, 6] keep lowest 5
        test = dice_utils.parse_keeps("3d6kl5", [1, 4, 6])
        self.assertIsNone(test)
        # Roll string with modifer no keeps
        test = dice_utils.parse_keeps("3d6+1", [1, 4, 6])
        self.assertDictEqual(test, {"keep": "kh", "value": 3})
        # Roll string with keep and modifier
        test = dice_utils.parse_keeps("3d6kh2+2", [1, 4, 6])
        self.assertDictEqual(test, {"keep": "kh", "value": 2})
        # Roll list contains different types
        test = dice_utils.parse_keeps("3d6", [1, "2", "test"])
        self.assertIsNone(test)
        # Roll list too short
        test = dice_utils.parse_keeps("3d6kh2", [1])
        self.assertIsNone(test)
        # Roll list empty
        test = dice_utils.parse_keeps("3d6kh2", [])
        self.assertIsNone(test)
        # Roll string empty
        test = dice_utils.parse_keeps("", [1, 2, 3])
        self.assertIsNone(test)
        # Roll string different type
        test = dice_utils.parse_keeps(1, [1, 2, 3])
        self.assertIsNone(test)

    def test_parseMods(self):
        """ Test Parsing Roll Mods """
        # Normal +1 mod
        test = dice_utils.parse_mods("2d6+1")
        self.assertDictEqual(test, {"op": "+", "value": 1})
        # Normal -1 mod
        test = dice_utils.parse_mods("2d6-1")
        self.assertDictEqual(test, {"op": "-", "value": 1})
        # Normal *1 mod
        test = dice_utils.parse_mods("2d6*1")
        self.assertDictEqual(test, {"op": "*", "value": 1})
        # Nomral /1 mod
        test = dice_utils.parse_mods("2d6/1")
        self.assertDictEqual(test, {"op": "/", "value": 1})
        # No mod found
        test = dice_utils.parse_mods("2d6")
        self.assertIsNone(test)
        # Non-string type passed
        test = dice_utils.parse_mods(1)
        self.assertIsNone(test)
        # Mod is non digit
        test = dice_utils.parse_mods("2d6+f")
        self.assertIsNone(test)
        # roll notation is only a mod
        test = dice_utils.parse_mods("+1")
        self.assertIsNone(test)

    @patch('dice_utils.randint')
    def test_sumRoll(self, mock_randint):
        """ Test Summing Rolls """
        # Normal Roll, no keeps, no mods
        roll = "3d6"
        mock_randint.side_effect = [1, 4, 6]
        test_a = dice_utils.sum_roll(roll)
        self.assertEqual(test_a, 11)
        mock_randint.side_effect = [1, 4, 6]
        test_b = dice_utils.sum_roll(roll, verbose=True)
        self.assertDictEqual(test_b, {
            'notation': '3d6',
            'rolls': [1, 4, 6],
            'keep': [1, 4, 6],
            'result': 11,
            'mod': None
        })
        # Normal Roll, keep highest 2, no mods
        roll = "3d6kh2"
        mock_randint.side_effect = [1, 4, 6]
        test_a = dice_utils.sum_roll(roll)
        self.assertEqual(test_a, 10)
        mock_randint.side_effect = [1, 4, 6]
        test_b = dice_utils.sum_roll(roll, verbose=True)
        self.assertDictEqual(test_b, {
            'notation': '3d6kh2',
            'rolls': [1, 4, 6],
            'keep': [4, 6],
            'result': 10,
            'mod': None
        })
        # Normal Roll, keep highest 2, +2 mod
        roll = "3d6kh2+2"
        mock_randint.side_effect = [1, 4, 6]
        test_a = dice_utils.sum_roll(roll)
        self.assertEqual(test_a, 12)
        mock_randint.side_effect = [1, 4, 6]
        test_b = dice_utils.sum_roll(roll, verbose=True)
        self.assertDictEqual(test_b, {
            'notation': '3d6kh2+2',
            'rolls': [1, 4, 6],
            'keep': [4, 6],
            'result': 12,
            'mod': '+2'
        })
        # invalid notation given
        roll = "3f6kh2+2"
        test_a = dice_utils.sum_roll(roll)
        test_b = dice_utils.sum_roll(roll, verbose=True)
        self.assertIsNone(test_a)
        self.assertIsNone(test_b)
        # invalid type given to rollnot param
        roll = 12
        test_a = dice_utils.sum_roll(roll)
        test_b = dice_utils.sum_roll(roll, verbose=True)
        self.assertIsNone(test_a)
        self.assertIsNone(test_b)

class TestDieClass(unittest.TestCase):
    def test_init(self):
        test_a = dice_utils.Die()               # Should default 1, 6
        test_b = dice_utils.Die.create(1, 2)    # Should set 1, 2
        test_c = dice_utils.Die.create(3)       # Should set 3, 6
        test_d = dice_utils.Die.create(20, 1)   # Should error because min > max
        test_e = dice_utils.Die.create("a", 4)    # Should error because min != type int
        test_f = dice_utils.Die.create(1, False)  # Should error because max != type int
        test_g = dice_utils.Die.create(max=20)    # Should default min 1, max 20
        test_h = dice_utils.Die.create(min=4)     # Should min 4, default max 6
        self.assertIsInstance(test_a, dice_utils.Die, "Default Min 1, Max 6")
        self.assertIsInstance(test_b, dice_utils.Die, "Min 1, Max 2")
        self.assertIsInstance(test_c, dice_utils.Die, "Min 3, Default Max 6")
        self.assertIsNone(test_d)
        self.assertIsNone(test_e)
        self.assertIsNone(test_f)
        self.assertIsInstance(test_g, dice_utils.Die)
        self.assertIsInstance(test_h, dice_utils.Die)

    @patch('dice_utils.randint')
    def test_roll(self, mock_randi):
        """ Test Die Class Roll """
        mock_randi.side_effect = [4, 18, -5]
        test_a = dice_utils.Die()
        test_b = dice_utils.Die.create(1, 20)
        test_c = dice_utils.Die.create(-20, 0)
        self.assertEqual(test_a.roll(), 4)
        self.assertEqual(test_b.roll(), 18)
        self.assertEqual(test_c.roll(), -5)

    @patch('dice_utils.randint')
    def test_getCurrent(self, mock_randi): 
        """ Test Die Class Get Current Side """
        mock_randi.side_effect = [4, 18, -5]
        test_a = dice_utils.Die()
        test_a.roll()
        test_b = dice_utils.Die.create(1, 20)
        test_b.roll()
        test_c = dice_utils.Die.create(-20, 0)
        test_c.roll()
        self.assertEqual(test_a.getCurrent(), 4)
        self.assertEqual(test_b.getCurrent(), 18)
        self.assertEqual(test_c.getCurrent(), -5)

if __name__ == "__main__":
    unittest.main()