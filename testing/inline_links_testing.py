from table import Table
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
    results = []
    brackets = []
    if '[' in text and ']' in text:
        brackets = [i for i, ch in enumerate(text) if ch == '[' or ch == ']']
    if brackets:
        for i in range(0, len(brackets), 2):
            try:
                results.append(text[brackets[i]+1:brackets[i+1]])
            except:
                pass
    return results

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
    currResLinks = checkResultForLinks(currRes)

def replaceRolls():
    pass

def checkResultForLinks(text:str):
    links = []
    for link in findLinksInString(text):
        l = {
            'text': link,
            'type': None,
            'sum': None,
            'table': None 
        }
        links.append(l)
    