## 6/3/2024
- Restructured folders and files.

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
