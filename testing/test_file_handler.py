import unittest
from unittest.mock import patch, MagicMock
from file_handler import FileHandler

class TestFileHandler(unittest.TestCase):
    @patch('file_handler.os.path.join', return_value="/mock/path/to")
    @patch('builtins.open', new_callable=unittest.mock.mock_open, 
        read_data='data')

    def test_loadFile_yaml(self):
        pass

    def test_loadFile_json(self):
        pass

    def test_loadFile_text(self):
        pass

    def test_loadFiles(self):
        pass
    
    def test_verifyFileFormat_yaml(self):
        pass

    def test_verifyFileFormat_json(self):
        pass

    def test_verifyFileFormat_text(self):
        pass

    def test_verifyFileExists(self, mock_exists):
        handler = FileHandler()

        # File Exists
        mock_exists.return_value = True
        self.assertTrue(self.handler.verifyFileExists('somefile.txt'))

        # File Does Not Exist
        mock_exists.return_value = False
        self.assertFalse(handler.verifyFileExists('someotherfile.txt'))
