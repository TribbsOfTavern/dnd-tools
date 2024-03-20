from table import Table
from table import InlineLink
import dice_utils as dice
import yaml
import glob

tables_dict = {}

def loadTablesFromYaml():
    """ Load the tables into the tables dict """
    all_files = glob.glob(".\\tables\\*.yaml")
    for file in all_files:
        with open(file, "r") as fobj:
            tables = list(yaml.load_all(fobj, Loader=yaml.FullLoader))
            for table in tables:
                tables_dict[table['table-name']] = Table(file, table)

def findLinksInString(text:str):
    links = []
    search = []
    brackets = []
    if '[' in text and ']' in text:
        brackets = [i for i, ch in enumerate(text) if ch == '[' or ch == ']']
    if brackets:
        for i in range(0, len(brackets), 2):
            try:
                search.append(text[brackets[i]+1:brackets[i+1]])
            except:
                pass
    for text in search:
        # Set the link text
        l_text = text
        # Set the link type
        l_type = None
        if "@" in text:
            l_type = 'table'
        elif dice.is_valid(text):
            l_type = 'roll'
        # Set the sum
        l_sum = None
        if l_type == 'roll' and dice.is_valid(text):
            l_sum = dice.sum_roll(text)
        if l_type == 'table':
            split = text.split('@')
            if split[0].isdigit(): l_sum = int(split[0])
            elif dice.is_valid(split[0]): l_sum = dice.sum_roll(split[0])
        # Set the table if there is any 
        l_table = None
        if l_type == 'table' and '@' in text:
            split = text.split('@')
            l_table = split[1]
        link = TableLink(l_text, l_tpye, l_sum, l_table)
        links.append(link)

    return links

# Retrieve Result
#
# Check Result For Rolls
#
# Replace Rolls with Roll Sum
#
# Check result for Link
#    
# If links exist
#   Eval Link for roll amount and table name
#
# For each roll amount, Retrieve Results
# If links do not exist
#   Return all results as a list  

def retrieveResult(table:Table, rolled:int):
    results = []
    currRes = table.getResults(rolled)
    currResLinks = findLinksInString(currRes)
    for link in currResLinks:
        pass
        
def replaceRolls():
    pass