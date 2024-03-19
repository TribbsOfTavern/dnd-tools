import glob
import yaml
from table import Table
import dice_utils as dice

# Variables
loaded_tables = []
loaded_files = []
current_table = None

def loadFilesFromDir(path):
    all_files = glob.glob(path)
    loaded_files = all_files

def loadTablesFromFiles():
    for file in loaded_files:
        with open(file, "r") as fobj:
            try:
                tables = list(yaml.load_all(fobj, Loaded=yaml.FullLoader))
                for table in tables:
                    self.app_loaded_tables.append(Table(file, table))
            except Exception as e:
                print(e)

def printLoadedTables():
    for table in loaded_tables:
        print(table.getName())

if __name__ == "__main__":
    path = "E:\\Projects\\Python\dnd-tools\\tables\\*.yaml"
    loadFilesFromDir(path)
    loadTablesFromFiles()
    print(loaded_files)
