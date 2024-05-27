"""
    Object models to be used with Rabke Roller App.
    Hopefully Written in a way that can be expanded later.
"""
from logger import setup_logger

main_logger, model_logger = setup_logger()

class Table:
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
        Return all information about the table if called as a string."
        This is a formatted output instead of a long string of gabled text
        making it easier to read the output of.
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
    def __init__(self, raw:str):
        """
        Initialize a result object that contains a key and 
        :param raw: String. containing the raw string of the result.
        """
        # TODO:
        # > Check for links in the result and store them
        # > method for returning a 'rolled' result
        self._raw = raw
        self._links = None

    @property
    def raw(self):
        """
        Return the raw string.
        :return: String containing the raw result string.
        """
        return self.raw

    @key.setter
    def raw(self, x:str) -> None:
        """
        Set the raw result string of the Result object.
        :param str: The raw string for the int result of the table.
        """
        self._raw = x

class Link:
    def __init__(self, link_text:str="", link_type:str="", link_sum:int=None,
    table:str=""):
        """
        Initialize a TableLink class that hold information about inline links
        :param link_text: String. The original text of the inline link as str.
        :param link_type: String. The type of inline table link, either 'roll' 
        or 'table'
        :param link_sum: Int. the sum of a roll or number of rolls on a table.
        :param table: String. Name of the table being referenced.
        :return: None
        """
        # Throw errors if parameters are incorrect:

        self.text = link_text
        self.type = link_type if link_type else None
        self.sum = link_sum
        self.table = table
        self.results = []
        
        # TODO: Move All To Link Validation function
        # Throw Errors if something is off.
        if self.type != 'roll' and self.type != 'table':
            raise TableInlineLinkError(f"Inline-Link {self.text} my have " + 
            "type 'roll' or 'table'.")
        if self.sum == None:
            raise TableInlineLinkError(f"Link {self.text} has no sum. An " +
             "integer must be provided.")
        if self.text == None:
            raise TableInlineLinkError(f"No inline link was provided. " + 
            "Expected String containing original text.")

"""
    Custom Errors Relating To Models objects
"""
class TableFormatError(Exception):
    """Raised when the table format is invalid."""
    pass

class TableInlineLinkError(Exception):
    """Raised when a table inline link format is invalid."""
    pass