'''
    Dice utils is a abasic library of functions for creating and rolling dice
    Specifically for interpretting roll notations.
    I may have over engineered this a bit.
'''
from random import randint
import re
from typing import List, Dict, Union, Optional

# Regularly used regex patterns
re_notation = re.compile("(\d+)d(\d+)($|(\D+)(\d+))($|(\D+)(\d))",
    re.IGNORECASE)
re_rolls = re.compile("(\d+)d(\d+)", re.IGNORECASE)
re_keeps = re.compile("(kh|kl)(\d+)", re.IGNORECASE)
re_mods = re.compile("(\+|\-|\*|\/)(\d+)", re.IGNORECASE)

class Die():
    ''' The just a bit overengineered die class 
        default is your standard six-sided die.
    '''
    def __init__(self, min:int=1, max:int=6) -> None:
        ''' Initialize the class, set the min and max rolls. 
            Current value defaults to lowest possible roll
        '''
        self.min = min
        self.max = max
        self.current_val = min

    def roll(self) -> None:
        ''' Roll the die and set current face value '''
        self.current_val = randint(self.min, self.max)

    def getCurrent(self) -> int:
        ''' Get the current face of the die '''
        return self.current_val

def parse_rolls(rollnote:str) -> Optional[Dict]:
    """
    Parse a roll notation string for dice rolls.

    This funciton extracts the rolls and then creates a list containing the
    results of the rolls. The roll notation should follow the format:
    'rXdY[kh|klZ][+|-|*|/Z]'.

    :param rollnote: The roll notation to evaluate.
    :return: a dictionary containing the list of rolls ('rolls') or None if no
        rolls are found in the roll notation.
    """
    rolls = re_rolls.search(rollnote)
    if rolls:
        return {'rolls': 
        [randint(1, 
        int(rolls.groups()[1])) for _ in range(int(rolls.groups()[0]))]}
    else:
        return None

def parse_keeps(rollnote:str, rolls:List[int]) -> Optional[Dict]:
    """
    Parse a roll notation string for keep highests/lowest 
    
    This function extracts the commands for keeping the high or low rolls and 
    the amount to be kept. The roll notation should follow the format:
    'rXdY[kh|klZ][+|-|*|/Z]'.

    :param rollnote: The roll notation to evaluate.
    :param rolls: A list of rolls as ints.
    :return: A dictionary containing the keep flag ('keep') and the amount to
        keep ('value') if a keep flag is found or None if no modifier is present
        in the roll notation.
    """
    keeps = re_keeps.search(rollnote)
    if keeps and int(keeps.groups()[1]) <= len(rolls):
        return {'keep': keeps.groups()[0], 'value': int(keeps.groups()[1])}
    else:
        return None

def parse_mods(rollnote:str) -> Optional[Dict]:
    """ 
    Parse a roll notation for modifiers
    
    This function extracts the modifier operation and value from a roll notation
    string. The roll notation should follow the format: 
    'rXdY[kh|klZ][+|-|*|/Z]'.

    :param rollnote: The roll notation to evaluate
    :return: A dictionary containing the modifier operation ('op') and value
        ('value') if a modifier is found or None if no modifier is present in 
        the roll notation.
    """
    mods = re_mods.search(rollnote)
    if mods:
        return {'op': mods.groups()[0], 'value': int(mods.groups()[1])}
    else:
        return None

def sum_roll(rollnote:str, verbose:bool=False) -> Union[Dict, int]:
    """ 
    Evaluate a roll notation and return the result.

    This function takes a roll notation string (e.g., 'r2d6kh1+2') and evaluates
    it according to the following rules:
    - 'rXdY': Roll X dice with Y sides each.
    - 'khZ' or 'klZ': Keep the highest (kh) or lowest (kl) Z rolls.
    - '+Z', '-Z', '*Z', '/Z': Add (or subtract, multiply, or divide) Z to the 
        result.

    :param rollnote: The roll notation to evaluate.
    :param verbose: If True, return a dictionary with all results.
    :return: The result of the roll notation evalluation.
    """ 
    rolls = parse_rolls(rollnote)
    keeps = parse_keeps(rollnote, rolls['rolls'])
    mods = parse_mods(rollnote)

    if not rolls: 
        return None

    #sort rolls and start results dict
    rolls['rolls'].sort()
    results = {
        "notation": rollnote,
        "rolls": rolls['rolls'],
        "keep": None,
        "mod": None,
        "result": None
    }

    # store the kept rolls
    if keeps:
        if keeps['keep'] == 'kh':
            results['keep'] = results['rolls'][-keeps['value']:]
        if keeps['keep'] == 'kl':
            results['keep'] = results['rolls'][:keeps['value']]
    # Sum the rolls
    if results['keep']:
        results['result'] = sum(results['keep'])
    else:
        results['result'] = sum(results['rolls'])
    # Apply modifier if any
    if mods:
        if mods['op'] == '+':
            results['result'] = results['result'] + mods['value']
            results['mod'] = mods['op'] + str(mods['value'])
        if mods['op'] == '-':
            results['result'] = results['result'] - mods['value']
            results['mod'] = mods['op'] + str(mods['value'])
        if mods['op'] == '*':
            results['result'] = results['result'] * mods['value']
            results['mod'] = mods['op'] + str(mods['value'])
        if mods['op'] == '/': 
            results['result'] = results['result'] // mods['value']
            results['mod'] = mods['op'] + str(mods['value'])

    if verbose:
        return results
    else:
        return results['result']

def is_valid(rollnote:str) -> bool:
    """
    Given a string, evaluate if it is a valid roll notation.

    :param rollnote: The string of roll notation to be checked.
    :return: True if the string is valid roll notation, False if the string
    if not valid roll notation.
    """
    return True if re_notation.match(rollnote) else False

# For testing
if __name__ == "__main__":
    rolls = [
        "1d6",
        "4d6kh3",
        "2d20kl1",
        "2d8kh1",
        "2d6+2",
        "2d6kh1+2",
        "2d100kh1/2",
        "2d50kl1*3",
        "3d6-4"
    ]

    for each in rolls:
        print(sum_roll(each))