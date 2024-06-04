"""
    FileHandler class
    - load file
    - load all files in dir
    - write to existing file
    - write to new file
"""
from logger import setup_logger
import yaml, json
import glob
import os

main_logger, models_logger, fhandler_logger = setup_logger()

class FileHandler:
    """
    Class dealing with reading, writing, and verifying files.
    Each instance of the application should only need a single instance of the 
    FileHandler class to operate.
    """
    def __init__(self, current_dir:str="./"):
        """
        Initialize the FileHandler, given a starting directory, and optionally
        available file extentions.
        :param current_dir: str. default directory to look for files.
        """
        self._working_dir = current_dir
        self._exts = ['yaml', 'json', 'txt']

        fhandler_logger.debug("FileHandler initialized.")

    @property
    def dir(self):
        return self._working_dir

    @dir.setter
    def setDirectory(self, dir):
        self._working_dir = dir

    def loadFile(self, filename, dir="") -> dict:
        """
        Given a filename and optionally a directory, read the file in and parse
        the data into a dictionary to be returned.
        :param filename: str. Name of the file to read.
        :opt param dir: str. Default is FileHandler._working_dir. Directory to 
        check for the file.
        :return: dict. Dictionary containing the file contents. Returns empty 
        dictionary if there is an error reading, or no file is found.
        """
        d = self._working_dir if not dir else dir
        path = os.path.join(d, filename)

        if (not self.verifyFileExists(filename, d) or
        not self.verifyFileExists(filename, d)):
            main_logger.error(f"{filename} could not be loaded.")
            return {}

        ext = filename.split('.')[-1]
        if ext == 'yaml':
            in_data = self._readYamlToDict(path)
        if ext == 'json':
            in_data = self._readJsonToDict(path)
        if ext == 'txt':
            in_data = self._readTextToDict(path)

        return in_data

    def loadFiles(self, dir="") -> list:
        """
        Given a directory path, read in all files within the dir and attempt to
        read all the files into a list as dictionarys and return that list.
        :param dir: str. Path to the directory to load files from.
        :return: list. List of dictionaries read in from files.
        """
        d = self._working_dir if not dir else dir
        all_files = glob.glob(dir)
        all_dicts = []
        for file in all_files:
            if file.split('.')[-1] in self._exts:
                fhandler_logger.debug(f"Loaded {file}")
                all_dicts.append(self.loadFile(file, d))
        
        return all_dicts

    def writeFile(self, output:dict, filename:str,
        dir:str="", format: str = "yaml") -> None:
        """
        Given a dictionary, filename, and optionally a directory, save a the 
        dictionary to a file. This can overwrite existing files.
        :param output: dict. The dictionary to be saved.
        :param filename: str. Name of the file to save dictionarty to.
        :opt param dir: str. Path of the directory to save dictionary to.
        """
        path = os.path.join(dir, filename)
        try:
            with open(path, 'w') as file:
                if format.lower() == 'yaml':
                    yaml.dump(output, file, default_flow_style=False)
                elif format.lower() == 'json':
                    json.dump(output, file, indent=4)
                elif format.lower() == 'txt':
                    file.write(output)
                else:
                    main_logger.error(f"{filename.split('.')[-1]} is an invalid"
                    + f" file extention. Please use one of {''.join(self._exts, ',')}")
        except IOError as e:
            filehandler_logger.error(f"Failed to write to file {path}: {e}")

    def verifyFileFormat(self, filename:str) -> bool:
        """
        Verify that a given file is using a proper extention.
        :param filename: str. Filename to be tested.
        :return: bool.
        """
        if not filename.split('.')[-1] in self._exts:
            main_logger.error(f"File extention {filename.split('.')[-1]} not" 
                + " compatible with application.")
            return False
        return True

    def verifyFileExists(self, filename:str, dir:str) -> bool:
        """
        Verify that the given file exists in the given directory
        This also call a check to verify the file format. If the format is
            invalid then the path is invalid.
        :param filename: str. Name of the file to check.
        :param dir: str. Path to check for the file.
        :return: bool.
        """
        if not self.verifyFileFormat(filename):
            main_logger.error(f"File path can not be verified because"
                + f" {filename} does not exist.")
            return False
        path = os.path.join(dir, filename)
        if not os.path.exists(path):
            main_logger.error(f"Path '{path}' is not valid.")
            return False
        return True

    def _readYamlToDict(self, path:str) -> dict:
        """
        Read a YAML file from a given filepath and return its contents as a
        dictionary.
        :param path: str. Path to the YAML file.
        :return: dict. Dictionary representing the contents of the YAML file.
        """
        try:
            with open(path, 'r') as file:
                return yaml.safe_load(file)
        except yaml.YAMLError as e:
            fhandler_logger.error(f"Error parsing YAML file {path}: {e}")
            return {}

    def _readJsonToDict(self, path) -> dict:
        """
        Read a JSON file from a given filepath and return its contents as a 
        dictionary.
        :param path: str. Path to the JSON file.
        :return: dict. Dictionary representing the contents of the JSON file.
        """
        try:
            with open(path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            fhandler_logger.error(f"Error deconding JSON from file {path}")
            return {}

    def _readTextToDict(self, path) -> dict:
        """
        Read a plain text file from a given filepath and return its contents as
        a dictionary.
        :param path: str. Path to the TXT file.
        return: dict. Dictionary representing the contents of the TXT file.
        """
        try:
            with open(path, 'r') as file:
                lines = file.readlines()
                data_dict = {}
                for line in lines:
                    key, value = line.split(':')
                    key = key.strip()
                    value = value.strip()
                    data_dict[key] = value
                return data_dict
        except Exception as e:
            fhandler_logger.error(f"An error occurred while reading the file "
            + f"{path}.")
            return {}
