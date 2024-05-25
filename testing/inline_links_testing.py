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
    """
    Find all the inline links within a result string and return them in order.
    Inline links are expected to be within brackets '[' and ']'.
    This function does not check if a table name is valid should one be provided.
    :param text: String. The string that may contain inline links.
    :return: List. Inline links as found within the 'text' string.
    """
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
        elif dice.is_valid(l_text):
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

        link = InlineLink(l_text, l_type, l_sum, l_table)
        links.append(link)

    return links

def retrieveResult(table:Table, rolled:int, depth:int=0):
    # Retrieve Result
    print_debug = False
    results = []
    try:
        res = table.getResult(rolled)
    except:
        pass
    results.append(res)
    depth = depth

    links = findLinksInString(table.getResult(rolled))


    # DEBUGGING
    if print_debug:
        if depth == 0:
            pmsg = f"{'DEPTH':^7} | {'LINK TEXT':^19} | {'TYPE':^7} | {'SUM':^10} |"
            pmsg += f"{'TABLE':^19} \n"
        else:
            pmsg = ""
        for link in links:
            pmsg += f"{depth:<7} | {link.text:19} | {link.type:7} | "
            pmsg += f"{link.sum:<10} | {link.table if link.table else '':19}\n" 
        print(pmsg)
    # END DEBUGGING


    for link in links:
        if link.type == 'table' and link.sum:
            t = retrieveTable(link.table)
            for i in range (0, link.sum):
                if t: results.extend(retrieveResult(t, 
                dice.sum_roll(t.getRollNote()), depth + 1))

    return results

def  retrieveTable(table_name:str) -> Table:
    return tables_dict[table_name] if table_name in tables_dict else None

def tableValidation() -> bool:
    for name, table in tables_dict.items():
        for i in range(1, len(table.results)):
            print(f"{name} -> {table.getResult(i)}")
            links = retrieveResult(table, i)
            for link in findLinksInString(links):
                if not link.type:
                    return False
                      

if __name__ == "__main__":
    loadTablesFromYaml()
    
    tableValidation()

    '''
    #Test Example
    test_table = "Test Table A"
    test = 8
    
    x = retrieveResult(tables_dict[test_table], test)
    msg = ' Test ' + str(test)
    print(f"{msg:_^60}")
    print(x , "\n")
    '''