import re
import random

# Roll Notation Rules
# [roll, ie 2d6] [kh|kl <digit>] [+|-|*|/ <digit]
# Check for valid roll -> store to var
# if roll look for keeps (kh|kl) -> store to var (pos int for highest, neg for lowest) 
# look for algebraic modifier -> store operator to var
# Look for algebraic modifer value -> store to var

test_cases = [
    "r1d6",         # valid
    "r2d6",         # valid
    "r2d20kl1",     # valid
    "r2d8kh1",      # valid
    "r2d6+2",       # valid
    "R1d15",        # valid
    "r2d6kh1+2",    # valid
    "r5d100kl2",    # valid
    "r3d4+2",       # valid
    "r3d4-2",       # valid
    "r3d4*2",       # valid
    "r3d4/2",       # valid
    "r2d6kh+2",     # not valid - no number after 'kh'
    "1d12",         # not valid - doesn't start with 'r'
    "testing",      # not valid - not roll notation
    "",             # not valid - empty string
    "1F12",         # not valid - not roll notation
    "r2d6+1d4"      # onlt r2d6+1 will be evaluated
]

test_pattern = re.compile("r(\d+)d(\d+)($|(\D+)(\d+))($|(\D+)(\d))", re.IGNORECASE)
test_dice_pat = re.compile("(\d+)d(\d+)", re.IGNORECASE)
test_keeps_pat = re.compile("(kh|kl)(\d+)", re.IGNORECASE)
test_mods_pat = re.compile("(\+|\-|\*|\/)(\d+)", re.IGNORECASE)

def outputToFile(output, filename):
    with open(filename, "w") as f:
        f.write(output)

def regexTesting(test_cases):
    out_results = ""

    print(f"{' Grouping Tests (re.match) ':-^60}")
    out_results += f"{' Grouping Tests (re.match) ':-^60}\n"
    for test in test_cases:
        pattern_matches = test_pattern.match(test)
        print(f"{test:<10}: {pattern_matches.groups() if pattern_matches != None else 'None'}")
        out_results += f"{test:<10}: {pattern_matches.groups() if pattern_matches != None else 'None'}\n"

    print(f"{' Roll Pattern Testing (re.search) ':-^80}")
    out_results += f"{' Roll Pattern Testing (re.search) ':-^80}\n"
    for test in test_cases:
        pattern_matches = test_dice_pat.search(test)
        print(f"{test:<10}: {pattern_matches.groups() if pattern_matches != None else 'None'}")
        out_results += f"{test:<10}: {pattern_matches.groups() if pattern_matches != None else 'None'}\n"

    print(f"{' Keeps Pattern Testing (re.search) ':-^80}")
    out_results += f"{' Keeps Pattern Testing (re.search) ':-^80}\n"
    for test in test_cases:
        pattern_matches = test_keeps_pat.search(test)
        print(f"{test:<10}: {pattern_matches.groups() if pattern_matches != None else 'None'}")
        out_results += f"{test:<10}: {pattern_matches.groups() if pattern_matches != None else 'None'}\n"

    print(f"{' Math Modifier Testing (re.search) ':-^80}")
    out_results += f"{' Math Modifier Testing (re.search) ':-^80}\n"
    for test in test_cases:
        pattern_matches = test_mods_pat.search(test)
        print(f"{test:<10}: {pattern_matches.groups() if pattern_matches != None else 'None'}")
        out_results += f"{test:<10}: {pattern_matches.groups() if pattern_matches != None else 'None'}\n"

    print(f"{' Roll Pattern Testing (re.findall) ':-^80}")
    out_results += f"{' Roll Pattern Testing (re.findall) ':-^80}\n"
    for test in test_cases:
        pattern_matches = test_dice_pat.findall(test)
        print(f"{test:<10}: {pattern_matches if pattern_matches != None else 'None'}")
        out_results += f"{test:<10}: {pattern_matches if pattern_matches != None else 'None'}\n"

    outputToFile(out_results, "regex_testing.txt")

def evalRollNotation(test_case):
    pat_rolls = re.compile("(\d+)d(\d+)", re.IGNORECASE)
    pat_keeps = re.compile("(kh|kl)(\d+)", re.IGNORECASE)
    pat_mods = re.compile("(\+|\-|\*|\/)(\d+)", re.IGNORECASE)
    reg_rolls = pat_rolls.search(test_case)
    reg_keeps = pat_keeps.search(test_case)
    reg_mods = pat_mods.search(test_case)
    #test_results = []
    eval_results = {}
    #test_results.append(reg_rolls.groups() if reg_rolls != None else '')
    #test_results.append(reg_keeps.groups() if reg_keeps != None else '')
    #test_results.append(reg_mods.groups() if reg_mods != None else '')

    if test_pattern.match(test_case) == None:
        return None
    # Add notation to the results dict
    eval_results["notation"] = test_case
    # add list of rolls to the results dict
    eval_results["rolls"] = None
    if reg_rolls != None:
        eval_results["rolls"] = [] 
        for i in range(int(reg_rolls.groups()[0])):
            eval_results["rolls"].append(random.randint(1, 
                int(reg_rolls.groups()[1])))
        eval_results["rolls"].sort()
    # add keep value to the results dict, neg to keep highest, pos for lowest
    eval_results["keep"] = None
    if reg_keeps != None:   
        eval_results["keep"] = reg_keeps.groups()
        if int(reg_keeps.groups()[1]) > len(eval_results["rolls"]):
            eval_results["keep"] = None
        else:
            eval_results["keep"] = int(reg_keeps.groups()[1])
    # add mod operator and mod value to results dict
    eval_results["mod_op"] = None
    eval_results["mod_val"] = None
    if reg_mods != None:
        eval_results["mod_op"] = reg_mods.groups()[0]
        eval_results["mod_val"] = int(reg_mods.groups()[1])
    # add roll results to the results dict
    eval_results["results"] = None
    if eval_results["keep"] != None:
        if reg_keeps.groups()[0] == "kh":
            eval_results["results"] = sum(eval_results["rolls"][-eval_results["keep"]:])
        elif reg_keeps.groups()[0] == "kl":
            eval_results["results"] = sum(eval_results["rolls"][:eval_results["keep"]])
    else:
        eval_results["results"] = sum(eval_results["rolls"])

    return eval_results

## Simplified evalRoll

if __name__ == "__main__":
    #regexTesting(test_cases)
    for test in test_cases:
        print(evalRollNotation(test))