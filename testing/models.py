"""
    Object models to be used with Rabke Roller App.
    Hopefully Written in a way that can be expanded later.
"""
import logger
import dice_utils

main_logger, model_logger, fhandler_logger = logger.setup_logger()

class Table:
    """
    Table instance to handle with all data partaining to tables. A loaded table
    must be loaded from a properly formatted yaml file.
    """
    def __init__(self, filename:str, loaded:dict) -> None:
        """
        Initialize A Table class containing the name, roll, results, and group
            that belong to the table.

        :param filename: A String of the filename that the table was loaded from
            this is used for the table group name.
        :param loaded: A dictionary containing the table information that should
            have specific information formatted for 'Table Roller' application
        """
        if not self._validate(loaded):
            #!!REMOVE raise TableFormateError("Table format is missing required keys.")
            # kill the initialize if not valid format.
            return

        self._filename = filename
        self._name = loaded['table-name']
        self._roll = loaded['roll']
        self._group = loaded['group'] if 'group' in loaded else ""
        self._results = loaded['result']

    def __str__(self):
        """
        Return all information about the table if called as a string.
        This is a formatted output instead of a long string of gabled text
        making it easier to read the output.
        :return: str. Formatted text containing all information about the table.
        """
        msg = f"Table: {self.name()}:^20\n"
        msg += f"filename: {self.filename()}\n"
        msg += f"roll: {self.roll()}\n"
        msg += f"group: {self.group()}\n"
        msg += f"result length: {self.length()}\n"
        msg += f"results :\n"
        for roll, res in self.results():
            msg += f"\t{roll}: {self. res.raw()}"
        return msg

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
        if not _resultExists(value):
            main_logging.error(f"Result Error: {value} not found within "+
                + f"results for table {self.name()}.")
            return ""
        return self.results[value].raw()

    def getResult(self, value:int) -> str:
        """ 
        Given an integer, return the given result from the results dictionary.
        :param x: Integer key to the result (value) to be found in the 
            dictionary.
        :return: The result in coresponding to the value given.
        """
        if not _resultExists(value):
            return ""
        return self.results[value].get()

    def _resultExists(self, value:int) -> bool:
        """
        Check if a result is within the table.\
        :param value: int. Value of a roll on a table to be check if exists.
        :return: bool.  
        """
        if value not in self.results():
            main_logger.error(f"Key {value} not found in table {self.name}"
                + " results.")
            return False
        return True

    def _validateTable(self, loaded:dict) -> bool:
        """
        Given the loaded dictionary with the expected table format, check if it
            is actually a valid table.
        """
        required_keys = ['table-name', 'roll', 'results']
        if not all(required_keys in loaded):
            main_logger.error("Table format missing one or more required" +
                f" keys {required_keys}")
            return False
        return True

class Result:
    """
    Result object handles all data regarding a result including linked
    references on other tables, and in-line rolls. This information is stored in
    created Link objects.
    """
    def __init__(self, raw:str):
        """
        Initialize a result object that contains a key and 
        :param raw: String. containing the raw string of the result.
        """
        self._raw = raw
        self._links = self._parseLinks(raw)

    def __str__(self):
        """
        Get a long formatted string containing all the information about the
            Result object. Formatted to readability.
        :return: str. A formated string containing all information about Result.
        """
        msg = f"Raw: {self.raw}\n"
        if not self._links:
            msg += "Links: None\n"
        else:
            for l_text, l_type in self._links:
                msg += f"{l_text}: {l_type}\n"
        return msg

    def _parseLinks(self, raw:str) -> dict:
        """
        Parse the raw sting for links and return a dictionary of them.
        dictionary key, value returns on {raw link: Link object}
        :return: dict. a dictionary of links within the raw string.
        """
        links = {}
        search = []
        brackets = []
        if '[' in text and ']' in text:
            brackets = [i for i, ch in enumerate(raw) if ch == '[' or ch == ']']
        if brackets:
            for i in range(0, len(brackets), 2):
                try:
                    search.append(text[brackets[i]+1:[i+1]])
                except:
                    pass
        for found in search:
            links[text] = Link(found)

    @property
    def raw(self):
        """
        Return the raw string.
        :return: String containing the raw result string.
        """
        return self.raw

    @raw.setter
    def raw(self, x:str) -> None:
        """
        Set the raw result string of the Result object.
        :param str: The raw string for the int result of the table.
        """
        self._raw = x

    def get() -> str:
        """
        Return a resolved result string.
        :return: str. A String that has been resolved, including linked table
        rolls and summed dice rolls.
        """
        # TODO: THIS
        pass

class Link:
    """
    Link object contains all information of a single stand alone roll or roll
    on another table reference. A link has a type of either 'roll' or 'table'.
    There will not be a reference to a Link of link_type 'roll'.
    """
    def __init__(self, text:str):
        """
        Initialize a TableLink class that hold information about inline links
        :param link_text: String. The original text of the inline link as str.
        """
        if not self._valid(text):
            return

        self._text = text
        self._type = 'table' if '@' in text else 'roll'
        self._roll = text if self._type == 'roll' else text.split('@')[0]
        self._table = "" if self._type == 'roll' else text.split('@')[1]

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

    def _valid(self, x:str):
        if not '@' in x or not dice_utils.is_valid(x):
            main_logger.error(f"{x} is not a valid link format.")
            return False
        return True

class Reslover:
    """
    Resolver takes the loaded dict of tables and is used to resolve rolled
    results, including nested refereces. Generally only one instance of a
    resolver should be needed for an app.
    """
    def __init__(self, tables: dict):
        """
        Initializing the resolver with a mapping of table names to Table
        instances.
        """
        self._tables = tables

    def get(self, result: Result) -> str:
        """
        Resolve a Result object, including any nested references.
        :param result: The Results object to resolve.
        :return: The resolved result string.
        """
        if not results.links:
            return result.raw()
        
        resolved_link = []
        for link in results.links:
            if link.link_type == 'roll':
                # TODO --  Return the raw and result of the roll as dict
                if link.text.is_digit():
                    # Amount of rolls
                    pass
                else:
                    # Roll notation to determin
                    pass
            elif link.link_type == 'table':
                # TODO -- Check this code to make sure it works fine.
                # Currently doesnt account for multiple rolls on a table.
                referenced_table = self.tables[link.table]
                referenced_roll = link.roll # roll needs to be summed by dice utils
                referenced_result = referenced_table.getResult(referenced_roll)
                resolved_link = self.get(referenced_result)
                resolved_links.append(resolved_link)

    def update(self, tables:dict):
        """
        Update the table dictionary for the Resolver object.
        """
        if not tables == self._tables: self._tables = tables
