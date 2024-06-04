import sys
import unittest
from unittest.mock import patch, MagicMock

from file_handler import FileHandler

class TestFileHandler(unittest.TestCase):
    @patch('file_handler.FileHandler._readYamlToDict')
    @patch('builtins.open', new_callable=unittest.mock.mock_open,
        read_data=
            """
            key: value
            key2:
                subkey: value
            """)
    def test_loadFile_yaml(self, mock_readYamlToDict, mock_open):
        #Setup
        handler = FileHandler()
        
        #Configure
        handler.verifyFileFormat = lambda x, y: True
        handler.verifyFileExists = lambda x, y: True

        mock_readYamlToDict.return_value = {
            'key': 'value',
            'key2': {
                'subkey': 'value'
            }
        }
        
        #Action
        result = handler.loadFile('test.yaml')
        
        #Result
        mock_open.assert_called_once_with('./test.yaml', 'r')
        mock_readYamlToDict.assert_called_once_with('./test.yaml')
        self.assertEqual(result, {'key': 'value', 'key2': {'subkey': 'value'}})

    @unittest.skip("TODO")
    def test_loadFile_json(self):
        pass

    @unittest.skip("TODO")
    def test_loadFile_text(self):
        pass

    @unittest.skip("TODO")
    def test_loadFiles(self):
        pass
    
    @unittest.skip("TODO")
    def test_verifyFileFormat_yaml(self):
        pass

    @unittest.skip("TODO")
    def test_verifyFileFormat_json(self):
        pass

    @unittest.skip("TODO")
    def test_verifyFileFormat_text(self):
        pass

    @unittest.skip("TODO")
    def test_verifyFileExists(self, mock_exists):
        handler = FileHandler()

        # File Exists
        mock_exists.return_value = True
        self.assertTrue(self.handler.verifyFileExists('somefile.txt'))

        # File Does Not Exist
        mock_exists.return_value = False
        self.assertFalse(handler.verifyFileExists('someotherfile.txt'))
