from table import Table
import dice_utils as dice

test_table_a = {
    "table-name": "Table A",
    "group": "testing",
    "roll": "1d3",
    "result": {
        1: "Result A",
        2: "Result B: [1@Sub Table B]",
        3: "Result C: [1d4@Sub Table B]",
        4: "[1d4] Result D: [2@Sub Table B]"
    }
}

test_table_b = {
    "table-name": "Sub Table B",
    "group": "testing",
    "roll": "1d4",
    "result": {
        1: "Subresult A",
        2: "Subresult B",
        3: "Subresult C",
        4: "Subresult D"
    }
}


# Load testing tables
tables = []
tables.append(Table(filename= "", loaded=test_table_a))
tables.append(Table(filename= "", loaded=test_table_b))

tables_dict = {}
for i in range(len(tables)):
    tables_dict[tables[i].getName()] = tables[i]


# print table instances
def test_printTablesByInstance():
    print(f"\n{'Tables by Instances':^40}")
    for i in range(len(tables)): 
        print(i, tables[i])

# print table instance by name
def test_printTablesByName():
    print(f"\n{'Tables by Name':^40}")
    for i in range(len(tables)):
        print(i, tables[i].getName())

# print tables dict, name: <Table> instance
def test_printTableDict():
    print(f"\n{'Table Dict':^40}")
    for name, inst in tables_dict.items():
        print(f"{name}: {inst}")

# Random rolls on Table A results:
def test_randomRollsTableA():
    print(f"""\n{'Random Rolls on "Table A"':^40} """)
    for i in range(4):
        roll = dice.sum_roll(tables_dict['Table A'].getRollNote())
        print(f"Roll #{i}: {tables_dict['Table A'].getResult(roll)}")

# Random rolls on Sub Table B
def test_randomRollsSubTableB():
    print(f"\n{'Random Rolls on Table B':^40}")
    for i in range(4):
        roll = dice.sum_roll(tables_dict['Sub Table B'].getRollNote())
        print(f"Roll #{i}: {tables_dict['Sub Table B'].getResult(roll)}")

# Print result for Table A
def test_printResultsForTableA():
    print(f"\n{'Results for Table A':^40}")
    for i in range(1, tables_dict['Table A'].getResultsLength() + 1):
        print(f"{i}: {tables_dict['Table A'].getResult(i)}")

# Print links for Table A results
def test_linksInResultForTableA():
    print(f"\n{'Parsing Table A Results':^40}")
    for i in range(1, tables_dict['Table A'].getResultsLength() + 1):
        result = tables_dict['Table A'].getResult(i)
        links = findLinksInString(result)
        print(f"{i}: {result}")
        if links:
            print(f"\t{findLinksInString(result)}")
            print(f"\t{[parseTableLink(x) for x in findLinksInString(result)]}")

# Given a string find Link in string
def findLinksInString(text:str):
    result = []
    brackets = []
    if '[' in text and ']' in text:
        brackets = [i for i, ch in enumerate(text) if ch == '[' or ch == ']']
    if brackets != "":
        links = []
        for i in range(0, len(brackets), 2):
            try:
                links.append(text[brackets[i]+1:brackets[i+1]])
            except:
                pass
    return links

# parse table link
def parseTableLink(text:str):
    res = {'text': text}
    s = text.split('@')
    if len(s) == 1:
        res['roll'] = s[0]
    elif len(s) == 2:
        res['roll'] = s[0]
        res['table'] = s[1]
    return res

# parse links and clean them
def cleanTableLinks(links: list):
    for link in links:
        # if the roll is a string that can become a digit, do so
        if link['roll'].isdigit(): 
            link['roll'] = int(link['roll'])
        # if the roll is a roll notation then it will get summed
        elif dice.is_valid(link['roll']): 
            link['roll'] = dice.sum_roll(link['roll'])
        # At this point the roll should be an int
        # If there is a table name attached to the link, roll on the link
        if 'table' in link:
            link['results'] = []
            for _ in range(link['roll']):
                roll_res = dice.sum_roll(
                    table_dict[link['table']].getRollNote())
                res = tables_dict[link['table']].getResult(roll_res)
                par = None
                
                link['results'].append()

def getAllResults(table:Table, depth:int = 0):
    space = "  "*depth
    results = []

    return results

def test_replacements():
    print(f"\n{'Getting All Results':^40}")
    test_res = tables_dict['Table A'].getResult(4)
    links = findLinksInString(test_res)
    parsed = [parseTableLink(e) for e in links]
    
    print(test_res)
    print(links)
    print(parsed)
    print(cleanTableLinks(parsed))

if __name__ == "__main__":
    test_replacements()
