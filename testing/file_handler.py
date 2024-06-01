"""
    FileHandler class
    - load file
    - load all files in dir
    - write to existing file
    - write to new file
"""
import logger
import yaml, json
import glob

main_logger, model_logger, fhandler_logger = logger.setup_logger()

class FileHandler:
    """
    Class dealing with reading, writing, and verifying files.
    Each instance of the application should only need a single instance of the 
    FileHandler class to operate.
    """
    def __init__(self, current_dir:str=".\\",
        exts:list=['yaml']):
        """
        Initialize the FileHandler, given a starting directory, and optionally
        available file extentions.
        :param current_dir: str. Directory 
        """
        self._working_dir = current_dir
        self._exts = exts

    @property
    def dir(self):
        return self._working_dir

    @dir.setter
    def setDirectory(self, dir):
        self._working_dir = dir

    def loadFile(self, filename, dir="") -> dict:
        d = self._working_dir if not dir else dir
        path = os.path.join(d, filename)

        if (not self.verifyFileExists(filename, d) or
        not self.verifyFileExists(filename, d)):
            main_logger.error(f"{filename} could not be loaded.")
            return {}

        with open(path, "r") as fobj:
            data = fobj.read('')

    def loadFiles(self, dir="") -> list:
        d = self._working_dir if not dir else dir
        all_files = glob.glob(dir)

    def writeFile(self, filename, dir=None) -> None:
        # TODO --
        pass

    def createFile(self, filename, dir=None) -> None:
        # TODO --
        pass

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

    def _readYamlToDict(self, path) -> dict:
        pass

    def _readJsonToDict(self, path) -> dict:
        pass

    def _readTextToDict(self, path) -> dict:
        pass