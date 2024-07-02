"""
    Object models to be used with Rabke Roller App.
    Hopefully Written in a way that can be expanded later.
"""
import dice_utils
import logger

main_logger, models_logger, fhandler_logger = logger.setup_logger()

class Link:
    """
    Link object contains all information of a single stand alone roll or roll
    on another table reference. A link has a type of either 'roll' or 'table'.
    There will not be a reference to a Link of link_type 'roll'.
    A Link object should be initialized using the 'create' static method.
    """
    @staticmethod
    def create(text: str, logs:bool=False):
        """
        Create a Link object given a string.
        :param link_text: String. The original text of the inline link as str.
        :return: Obj. If Link is valid, return the link obj. If link is not
        valid, return None.
        """
        if not Link._valid(text):
            return None
        
        link = Link()
        link._logging = logs
        link._text = text
        link._type = 'table' if '@' in text else 'roll'
        link._roll = text if link._type == 'roll' else text.split('@')[0]
        link._table = '' if link._type == 'roll' else text.split('@')[1]
        return link

    def __init__(self):
        """
        Initialize a TableLink class that hold information about inline links
        :param link_text: String. The original text of the inline link as str.
        """

    @property
    def text(self) -> str:
        return self._text

    @property
    def link_type(self) -> str:
        return self._type

    @property
    def roll(self) -> str:
        return self._roll

    @property
    def table(self) -> str:
        return self._table

    def getDict(self) -> dict:
        """
        :return: dict. Returns all information within the object as a dict.
        """
        return {
            'text': self._text,
            'type': self._type,
            'roll': self._roll,
            'table': self._table
        }

    def _valid(text:str):
        """
        Validate the string is formated correctly for Link use.
        """
        # Invaalid type
        if not isinstance(text, str):
            if self._logging:
                main_logger.error(f'Expected string, recieved {type(type)}')
            return False
        # invalid dice roll with no table
        if not "@" in text and not dice_utils.is_valid(text):
            if self._logging:
                main_logger.error(f'{text} is invalid link.')
            return False
        if '@' in text and (not dice_utils.is_valid(text.split('@')[0]) and
        not text.split('@')[0].isdigit()):
            if self._logging:
                main_logger.error(f'1. Roll on table is not a valid roll'
                + ' notation or digit.')
            return False
            
        return True

class Result:
    """
    Result object handles all data regarding a result including linked
    references on other tables, and in-line rolls. This information is stored in
    created Link objects.
    """
    def __init__(self):
        """
        Initialize a result object that contains a raw string, and any links.
        Use static method Result.create() to create a Result object.
        """

    @staticmethod
    def  create(text:str, logs:bool=False):
        if not isinstance(text, str):
            if logs:
                main_logger.error("Result object expected string, recieved"
                + f" {text}.")
            return None

        result = Result()
        result._logging = logs
        result._text = text
        result._links = result.parseLinks(text)
        return result

    def parseLinks(self, text:str) -> dict:
        """
        Parse the raw sting for links and return a dictionary of them.
        dictionary key, value returns on {raw link: Link object}
        :return: dict. a dictionary of links within the raw string.
        """

        if not '[' in text or not ']' in text:
            return None

        links = {}
        search = []
        brackets = []
        if '[' in text and ']' in text:
            brackets = [i for i, ch in enumerate(text) 
            if ch == '[' or ch == ']']
        if brackets:
            for i in range(0, len(brackets), 2):
                try:
                    search.append(text[brackets[i]+1:brackets[i+1]])
                except:
                    pass
        for found in search:
            links[found] = Link.create(found)
        
        return links if links else None

    @property
    def text(self):
        """
        Return the raw string.
        :return: String containing the raw result string.
        """
        return self._text

    @property
    def links(self):
        """
        Return the links within the Result object.
        :return: dict. A Dictionary containing all links, empty dict '{}' if
        none.
        """
        return self._links

    @text.setter
    def text(self, text:str) -> None:
        """
        Set the raw result string of the Result object. Setting the text will
        also set links within the text.
        :param str: The raw string for the int result of the table.
        """
        if not isinstance(text, str):
            self._text = ""
            return

        self._text = text

        self._links = self.parseLinks(self._text)

    def toDict(self) -> dict:
        """
        Return the object variables as a dict.
        :return: dict. {"raw": x:str, "links": y:list[Link]}
        """
        return {"text": self._text, "links": self._links}

class Table:
    """
    Table instance to handle with all data partaining to tables. A loaded table
    must be loaded from a properly formatted yaml file.
    """
    def __init__(self) -> None:
        """
        Initialize A Table class containing the name, roll, results, and group
            that belong to the table.
        The Table.create method should be used to validate and initialize.
        """

    @staticmethod
    def create(loaded:dict, filename:str=""):
        """
        Create and validate a table object.
        :param loaded: A dictionary containing the table information that should
            have specific information formatted for 'Table Roller' application
        :param filename: A String of the filename that the table was loaded from
            this is used for the table group name.
        """

        table = Table()

        if not table.validateTable(loaded):
            return None

        table._filename = filename
        table._name = loaded['table-name']
        table._roll = loaded['roll']
        table._group = loaded['group'] if 'group' in loaded else ""
        table._results = {}

        for roll, res in loaded['results'].items():
            table._results[roll] = Result.create(res)

        return table

    @property
    def filename(self) -> str:
        """
        Returns the path and filename the Table was loaded from.
        :return: A string containing the path + filename of Table instance.
        """
        return self._filename

    @property
    def name(self) -> str:
        """
        Return the name of the table.
        :return: A string containing the name of the table. 
        """
        return self._name

    @property
    def roll(self) -> str:
        """
        Return the roll notation for the table.
        If the roll notation of the table is set to 'length' it should return
            a string formatted to 1d<length of the results dict>
        :return: A string containing the roll notation for the table.
        """
        return f"1d{str(len(self.results))}" if self._roll == 'length' else self._roll

    @property
    def group(self) -> str:
        """
        Return the group of the table.
        :return: A string containing the group name of the table.
        """
        return self._group

    @property
    def results(self) -> dict:
        """
        Return the dictionary of results stored in the table.
        :return: Dictionary containing the key:value
            ({roll result string: raw result string})  
        """
        return self._results

    @property
    def length(self) -> int:
        """
        Return the length of the results dictionary.
        :return: an integer representing the length of the results dictionary.
        """
        return len(self.results)

    def getRawResult(self, value:int) -> str:
        """
        Return a dictionary of results stored in the table, replacing the result
            object with the result object's raw string.
        :param value: int. value within the results range to retrieve,
        :return: str. Raw string of the result, if valid, empty string if not
            valid.
        """
        if not self.resultExists(value):
            if self._logging:
                main_logger.error(f"Result Error: '{value}' not found within "
                + f"results for table {self.name}.")
            return None
        return self.results[value].text

    def getResult(self, value:int) -> Result:
        """ 
        Given an integer, return the given result from the results dictionary.
        :param x: Integer key to the result (value) to be found in the 
            dictionary.
        :return: The Result object in coresponding to the value given.
        """
        if not self.resultExists(value):
            return None
        return self.results[value]

    def resultExists(self, value:int) -> bool:
        """
        Check if a result is within the table.\
        :param value: int. Value of a roll on a table to be check if exists.
        :return: bool.  
        """
        if value not in self.results:
            if self._logging:
                main_logger.error(f"Key {value} not found in table {self.name}"
                + " results.")
            return False
        return True

    def validateTable(self, loaded:dict) -> bool:
        """
        Given the loaded dictionary with the expected table format, check if it
            is actually a valid table.
        """
        required_keys = ['table-name', 'roll', 'results']
        
        # Check to make sure all required keys are in loaded dictionary.
        for key in required_keys:
            if not key in loaded:
                if self._logging:
                    main_logger.error(f"Table format missing required key "
                    + f"{key}.")
                return False

        if not isinstance(loaded['table-name'], str):
            return False
        if not isinstance(loaded['roll'], str):
            return False
        if not isinstance(loaded['results'], dict):
            return False
        
        # Check that roll is a valid roll or set to 'length'        
        if (not dice_utils.is_valid(loaded['roll']) and 
        not loaded['roll'] == 'length'):
            if self._logging:
                main_logger.error(f"Table key 'roll' must be a valid roll or"
                + f"'length'. Instead recieved {loaded['roll']}")
            return False 

        return True

class Resolver:
    """
    Resolver takes the loaded dict of tables and is used to resolve rolled
    results, including nested refereces. Generally only one instance of a
    resolver should be needed for an app.
    """
    def __init__(self, tables:dict={}, logs:bool=False):
        """
        Initializing the resolver with a mapping of table names to Table
        instances.
        """
        self._tables = tables
        self._logging = logs

    def get(self, result:Result, depth:int=0) -> str:
        """
        Given a Result object, clean it, and return results including results
        rolled on another table.
        """
        dep = depth
        if not result.links:
            return result.text
        else:
            temp_text = result.text
            print(f"{temp_text}")
            for l, link in result.links.items():
                if link.link_type == "roll":
                    r = dice_utils.sum_roll(link.roll)
                    print(f"{r} -> {link.text}")
                    temp_text = temp_text.replace(link.text, str(r), 1)                    
                elif link.link_type == 'table':
                    temp_result = []
                    amount = 0
                    
                    amount = link.roll
                    if dice_utils.is_valid(link.roll):
                        amount = dice_utils.sum_roll(link.roll)

                    temp_text = temp_text.replace(link.text,
                    f"{amount} on {link.table}", 1)

                    for _ in range(int(amount)):
                        table_roll = dice_utils.sum_roll(
                            self._tables[link.table].roll)
                        temp_res = self._tables[link.table].getResult(
                            table_roll)
                        temp_result.append(temp_res)
                    
                    spacer = "  "
                    for inline in temp_result:
                        inline_result = self._tables[link.table].getResult(
                        dice_utils.sum_roll(self._tables[link.table].roll))
                        temp_text += "\n\t"
                        temp_text += self.get(inline_result, depth=dep+1)
            
            return temp_text                        

    def update(self, tables:dict):
        """
        Update the table dictionary for the Resolver object.
        """
        if not tables == self._tables: self._tables = tables

    @property
    def tables(self):
        """
        Retrieve tables currently loaded within the Resolver object.
        """
        return self._tables