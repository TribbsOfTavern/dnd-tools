class TableFormatError(Exception):
    """Raised when the table format is invalid."""
    pass

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
        if 'table-name' not in loaded: 
            raise TableFormatError(
                "Table Format Invalid. No 'table-name' found."
            )
        elif 'roll' not in loaded:
            raise TableFormatError(
                "Table Format Invalid. No 'roll' found."
            )
        elif 'result' not in loaded: 
            raise TableFormatError(
                "Table Format Invalid. No 'result' found."
            )

        self.name = loaded['table-name']
        self.roll = loaded['roll']
        self.results = loaded['result']
        if 'group' in loaded:
            self.group = loaded['group']

    def getName(self) -> str:
        """
        Return the name of the table.

        :return: A string containing the name of the table. 
        """
        return self.name

    def getGroup(self) -> str:
        """
        Return the group of the table.

        :return: A string containing the group name of the table.
        """
        return self.group

    def getResult(self, x:int) -> str:
        """ 
        Given an integer, return the given result from the results dictionary.

        :param x: Integer key to the result (value) to be found in the 
            dictionary.
        :return: The result in coresponding to the value given. Otherwise return
            -1 if no result is found.
        """
        try:
            if x in self.results:
                return self.results[x]
            else:
                raise Exception(f"No value found for key {x}")
        except Exception as e:
            print(e)

    def getRollNote(self) -> str:
        """
        Return the roll notation for the table.

        :return: A string containing the roll notation for the table.
        """
        return self.roll

    def getAllResults(self) -> dict:
        """
        Return the dictionary of results stored in the table.

        :return: Dictionary containing the key:value pairs relating to the
            results. 
        """
        return self.results

    def getResultsLength(self) -> int:
        """
        Return the length of the results dictionary.

        :return: an integer representing the length of the results dictionary.
        """
        return len(self.results)