## 6/1/2024
- FileHandler: added verifying for file format and file exists
- FileHandler: added _readYamlToDict(), _readJsonToDict(), _readTextToDict()
- Filehandler: added loadFile(), loadFiles

## 5/30/2024
- file_handler.py created to handle file specific tasks.
- fhandler logger added

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
