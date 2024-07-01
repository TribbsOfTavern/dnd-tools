## 7/1/2024
app.py: added loadFiles() for loading entire directories of table files.

## 6/26/2024
- app.py initiates correct GUI components
- app.py: added func checkForProblems which checks all loaded tables for problems and output that info into Error Logs tab textbox.
- added extention .yml handling for YAML files.
- added Tools menu
- added function to clear Error Logs Tab
- added function to clear Roll Logs Tab

## 6/20/2024
- app.py created
- app.py: added TableRollerApp class.
- app.py: added class funcs, init, initWidgets, loadFromFile, TableConstruction, onTableSelection, onButtonRoll, updateTableList, updateResultLIst, updateTextRolls, updateTextLogs, doNothing, runApp, exitApp
- app.py: Single files load successfully

## 6/15/2024
- models.py rewrite, error handling added, Resolver class fleshed out.
- tests/test_models.py added and fleshed out.
- [Note] Was unsure how to go about unit testing Resolver. It was tested in a throw away file.

## 6/8/2024
- dice_utils.py: Added more error handling.

## 6/6/2024
 - dice_utils.py added to /dev/
 - tests/test_dice_utils.py added

## 6/5/2024
- file_handler.py: Removed readFileFromText as it too easily allows format breaks. Will be added back at a later date.
- file_handler.py: FileHandler.verifyFileFormat renamed to verifyFileExtention
- tests/test_file_handler.py: Unit tests for file_handler.py added 

## 6/4/2024
- Fixed file structure, learned a lot of nitpicks about imports. Working as intended now.

## 6/3/2024
- Restructured folders and files.
- Restructured broke logger.py.

## 6/2/2024
- logger.py: Fixed bug with logging format.

## 6/1/2024
- FileHandler: added verifying for file format and file exists
- FileHandler: added _readYamlToDict(), _readJsonToDict(), _readTextToDict()
- Filehandler: added loadFile(), loadFiles
- FileHandler: added writeFile()
- FileHandler: Removed createFile(), as writeFile() can both create and overwrite files.
- models.py: Removed custom exceptions. They are no longer needed.
- UnitTesting: Started learning and writing unit testing for models.py
- UnitTesting: Started learning and writing unit testing for file_handler.py

## 5/30/2024
- FileHandler: file_handler.py created to handle file specific tasks.
- logger: fhandler logger added

## 5/29/2024
- Remembered I created a change log.
- Proceeded with major overhauls of the projects starting with Table, Results, and Links.
- Added Resolver Object to models.py to resolve nested Results

## 2/27/2024
** CHANGELOG.MD **
New change log added.

- Removed TableRoller.addResults, TableRoller.logResults
- Added TableRoller.addResultToLog
- Changed TableRoller.rollOnTable to roll the correct number of times, and add each result with TableRoller.addResultToLog
 