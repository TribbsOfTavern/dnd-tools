import sys, io, yaml, json
import unittest
from unittest.mock import patch, MagicMock

from file_handler import FileHandler

class TestFileHandler(unittest.TestCase):
    mock_yaml_file = """
    "Key A": "Value 1"
    "Key B":
        "Subkey C": "Subvalue 2"
    """

    mock_json_file = """
    {"Key A": "Value 1", "Key B": {"Subkey C": "Subvalue 2"}}
    """

    mock_text_file = """
    Key A: Value 1
    Key B:
        Subkey C: Subvalue 2
    """

    expected_file_to_dict = {
        "Key A": "Value 1",
        "Key B": {
            "Subkey C": "Subvalue 2"
        }
    }

    @patch('builtins.open', new_callable=MagicMock)
    def test_readYamlToDict(self, mock_open):
        """ Test reading YAML file to Dict """
        # Setup
        handler = FileHandler()
        mock_open.return_value.__enter__.return_value = self.mock_yaml_file
        # Actions
        result = handler.readYamlToDict("dummy_file.yaml")
        # Asserts
        self.assertEqual(mock_open.call_count, 1)
        self.assertEqual(result, self.expected_file_to_dict)

    @patch('builtins.open', new_callable=MagicMock)
    def test_readJsonToDict(self, mock_open):
        """ Test reading JSON file to dict """
        # Setup
        handler = FileHandler()
        mock_open.return_value.__enter__.return_value = self.mock_json_file
        # Actions
        result = handler.readJsonToDict("dummy_file.json")
        # Asserts
        self.assertEqual(mock_open.call_count, 1)
        self.assertEqual(result, self.expected_file_to_dict)

    @patch('file_handler.FileHandler.readYamlToDict', new_callable=MagicMock)
    @patch('file_handler.FileHandler.readJsonToDict', new_callable=MagicMock)
    def test_loadFile(self, mock_readYamlToDict, mock_readJsonToDict):
        """ Test loading file """
        # Setup
        handler = FileHandler()
        handler.verifyFileExists = lambda x, y: True
        handler.verifyFileExtention = lambda x: True
        file_yaml = "test_file.yaml"
        file_json = "test_file.json"
        file_text = "test_file.txt"
        mock_readYamlToDict.return_value = self.expected_file_to_dict
        mock_readJsonToDict.return_value = self.expected_file_to_dict
        # Result
        result_yaml = handler.loadFile(file_yaml)
        result_json = handler.loadFile(file_json)
        result_text = handler.loadFile(file_text)
        # Asserts
        self.assertEqual(mock_readYamlToDict.call_count, 1)
        self.assertEqual(mock_readJsonToDict.call_count, 1)
        self.assertEqual(result_yaml, self.expected_file_to_dict)
        self.assertEqual(result_json, self.expected_file_to_dict)
        self.assertEqual(result_text, None)
        
    
    @patch('file_handler.FileHandler.loadFile', new_callable=MagicMock)
    @patch('glob.glob', new_callable=MagicMock)
    def test_loadFiles(self, mock_glob, mock_loadedFile):
        """ Test Loading multiple files """
        # Setup
        handler = FileHandler()
        mock_glob.return_value = [
            "test_file_a.yaml", "test_file_b.json", "test_file_c.txt"
        ]
        mock_loadedFile.return_value = self.expected_file_to_dict
        # Resulls
        result = handler.loadFiles('dummy')
        # Asserts
        self.assertEqual(result, [
            self.expected_file_to_dict,
            self.expected_file_to_dict])
    
    def test_verifyFileExtention(self):
        """ Test file extention verify """
        # Setup
        handler = FileHandler("", exts=['yaml', 'json', 'test'])
        verify = lambda x: handler.verifyFileExtention(x)
        # Results
        
        # Asserts
        self.assertTrue(verify('test.yaml'))
        self.assertTrue(verify('test.json'))
        self.assertTrue(verify('test.test'))
        self.assertFalse(verify('test.txt'))
        self.assertFalse(verify('test.exe'))
        self.assertFalse(verify('.yaml'))

    @patch('os.path.join', new_callable=MagicMock)
    @patch('os.path.exists', new_callable=MagicMock)
    def test_verifyFileExists(self, mock_pathExists, mock_pathJoin):
        """ Test file exists verify """
        # Setup
        handler = FileHandler(current_dir="./", exts=['yaml'])
        join_path = lambda f, d: str(d) + str(f)

        # File Extention Accepted, Path Exists True | assert True
        m_file = "test.yaml"
        m_dir = "some\\path\\to\\"
        mock_pathJoin.return_value = join_path(m_file, m_dir)
        mock_pathExists.return_value = True
        self.assertTrue(handler.verifyFileExists(m_file, m_dir))

        # File Extention Not Accepted, Path Exist True | assert False
        m_file = "test.txt"
        m_dir = "some\\path\\to\\"
        mock_pathJoin.return_value = join_path(m_file, m_dir)
        mock_pathExists.return_value = True
        self.assertFalse(handler.verifyFileExists(m_file, m_dir))

class TestWriteFiles(unittest.TestCase):
    def setUp(self):
        self.handler = FileHandler()
        self.output_dict = {
            "Key A": "Value 1",
            "Key B": {
                "Subkey C": "Subvalue 2"
            }
        }

    @patch('builtins.open', new_callable=MagicMock)
    def test_writeFile_yml(self, mock_open):
        """ Test writing to a YAML file. """
        # Setup
        mock_file = io.StringIO()
        mock_open.return_value.__enter__.return_value = mock_file
        f_name = "test_output.yaml"
        # Action
        self.handler.writeFile(self.output_dict, f_name, dir="", format="yaml")
        
        mock_file.seek(0)
        content = mock_file.read()
        expected_output = yaml.dump(self.output_dict, default_flow_style=False)
        # Assert
        self.assertEqual(content, expected_output)

    @patch('builtins.open', new_callable=MagicMock)
    def test_writeFile_json(self, mock_open):
        """ Test writing to a JSON file """
        # Setup
        mock_file = io.StringIO()
        mock_open.return_value.__enter__.return_value = mock_file
        f_name = "test_output.json"
        # Action
        self.handler.writeFile(self.output_dict, f_name, dir="", format="json")
        
        mock_file.seek(0)
        content = mock_file.read()
        expected_output = json.dumps(self.output_dict, indent=4)
        # Assert
        self.assertEqual(content, expected_output)

if __name__ == '__main__':
    unittest.main()