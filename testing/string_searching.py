test_str = "this is a test [1d6] string with some [1@Some Table]["

def findLinksInString(text:str) -> None:
    """
    Give a string find all substrings incased within brackets and 
    """
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

def parseTableLink(text:str):
    """
    Given a string check if it contains a table name.
    Return roll and table name
    """
    res = {}
    s = text.split('@')
    if len(s) == 1:
        res['roll'] = s[0]
    elif len(s) == 2:
        res['roll'] = s[0]
        res['table'] = s[1]
    return res

print(findLinksInString(test_str))