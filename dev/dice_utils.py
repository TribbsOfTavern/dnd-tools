'''
    Dice utils is a abasic library of functions for creating and rolling dice
    Specifically for interpretting roll notations.
    I may have over engineered this a bit.
'''
import re
import logger
from random import randint
from typing import List, Dict, Union, Optional

main_logger, models_logger, fhandler_logger = logger.setup_logger()

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
    def __init__(self) -> None:
        ''' Initialize the class, set the min and max rolls. 
            Current value defaults to lowest possible roll

            :param min: int. min number on the sides of a die. Must be lower
                than max. Default: 1
            :param max: int. max number of the sides of a die. Must be higher 
                than min. Default: 6
        '''
        self.min = 1
        self.max = 6
        self.current_val = 1

    @staticmethod
    def create(min:int=1, max:int=6):
        if not isinstance(min, int) or not isinstance(max, int):
            main_logger.error(f"Min and Max expected type int. "
                + f"Given type {type(min)} for min."
                + f" Given type {type(max)} for max.")
            return None
        if min >= max:
            main_logger.error("Die class param error. min must be lower than"
                + f" max. Given min {min} not less than given max {max}.")
            return None
        if max <= min:
            main_logger.error("Die class param error. max must be higher than"
                + f" min. Given max {max} not higher than given {min}.")
            return None

        created_die = Die()
        created_die.min = min
        created_die.max = max
        created_die_current_val = min
        return created_die

    def __str__(self):
        r_str = f"Die Objects: Min: {self.min} | Max: {self.max} |"
        r_str += f" Current: {self.current_val}"
        return r_str

    def roll(self) -> int:
        ''' Roll the die and set current face value '''
        self.current_val = randint(self.min, self.max)
        return self.current_val

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
    if not isinstance(rollnote, str):
        main_logger.error(f"Invalid type {type(rollnote)}. Expected type str.")
        return None
    if not rollnote:
        main_logger.error(f"Empty str. Expected str containing roll notation.")
        return None
    if not is_valid(rollnote):
        main_logger.error(f"Invalid roll notation passed {rollnote}.")
        return None

    rolls = re_rolls.search(rollnote)
    
    if not is_valid(rollnote):
        return None
    if not rolls:
        return None
    
    return {'rolls': [randint(1, 
        int(rolls.groups()[1])) for _ in range(int(rolls.groups()[0]))]}

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
    if not all(isinstance(r, int) for r in rolls):
        main_logger.error(f"Invalid type passed in rolls. Expected list of int"
            + " types.")
        return None
    if not isinstance(rollnote, str):
        main_logger.error(f"Invalid type {type(rollnote)}. Expected type str.")
        return None
    if not rollnote:
        main_logger.error(f"Empty str. Expected str containing roll notation.")
        return None
    if not is_valid(rollnote):
        main_logger.error(f"Invalid roll notation passed {rollnote}.")
        return None

    keeps = re_keeps.search(rollnote)
    if not keeps:
        return {'keep': 'kh', 'value': len(rolls)}
    if not (int(keeps.groups()[1]) <= len(rolls)):
        main_logger.error(f"Length of found groups longer than length of" 
            + " rolls.")
        return None

    return {'keep': keeps.groups()[0], 'value': int(keeps.groups()[1])}

def parse_mods(rollnote:str) -> Optional[Dict]:
    """ 
    Parse a roll notation for modifiers
    
    This function extracts the modifier operation and value from a roll notation
    string. The roll notation should follow the format: 
    'rXdY[kh|klZ][+|-|*|/M]'.

    :param rollnote: The roll notation to evaluate
    :return: A dictionary containing the modifier operation ('op') and value
        ('value') if a modifier is found or None if no modifier is present in 
        the roll notation.
    """
    if not isinstance(rollnote, str):
        main_logger.error(f"Invalid type {type(rollnote)}. Expected type str.")
        return None
    if not is_valid(rollnote):
        main_logger.error(f"Invalid roll notation passed {rollnote}.")
        return None

    mods = re_mods.search(rollnote)
    if not mods:
        return None

    return {'op': mods.groups()[0], 'value': int(mods.groups()[1])}

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
    if not isinstance(rollnote, str):
        main_logger.error("Invalid type passed as roll notation:"
            + f"{type(rollnote)}. Expected type str")
        return None
    if not isinstance(verbose, bool):
        main_logger.error(f"Invalid type passed as verbose: {type(verbose)}."
            + "Expected tyoe bool")
        return None
    if not is_valid(rollnote):
        main_logger.error(f"Passed roll notation {rollnote} is not valid.")
        return None

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