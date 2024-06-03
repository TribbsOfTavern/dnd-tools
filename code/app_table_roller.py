'''
    Name: 
        Tribbs' Table Roller
    Desc: 
        Loads in formatter YAML files from specified folder and allows user to
    select loaded tables and roll on them. Should be able to also roll linked 
    tables from the loaded table if applicable. 
'''
import tkinter as tk
from tkinter import ttk
import yaml
import glob
from typing import Dict, Literal, Optional
from table import Table, TableFormatError
from dice_utils import sum_roll as rollDice
from dice_utils import is_valid as isRollValid

class TableRoller():
    def __init__(self) -> None:
        ''' Initialize the app '''
        # instance variables
        self.debug = True
        self.app_loaded_files = []
        self.app_loaded_tables = []
        self.app_selected_table = -1
        self.app_current_table_info = None

        # Window initialization file Loading
        self.initWindow()
        self.loadYamlFiles()
        self.loadTablesFromFiles()

        self.run()

    def initWindow(self) -> None:
        ''' Initialize app window, load and configure widgets, load configs '''
        self.root = tk.Tk()
        self.root.title("Tribbs' Table Roller")
        self.root.geometry("800x600")
        self.root.iconbitmap("../assets/py-app-icon.ico")

        # Menu Bar
        self.menu_bar = tk.Menu()

        # Create a file menu
        self.menu_file = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_file.add_command(label="Reload Tables",
            command=self.doNothing)
        self.menu_file.add_command(label="Load Tables From...", 
            command=self.doNothing)
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Exit", command=self.exitApplication)
        self.menu_bar.add_cascade(label="File", menu=self.menu_file)

        # Create a Debug Menu
        if self.debug:
            self.menu_debug = tk.Menu(self.menu_bar, tearoff=0)
            self.menu_debug.add_command(label="Print Loaded Files", 
                command=self.menuDebugPrintFiles)
            self.menu_debug.add_command(label="Print Loaded Tables",
                command=self.menuDebugPrintTables)
            self.menu_debug.add_command(label="Print Selected Table",
                command=self.menuDebugPrintSelectedTable)
            self.menu_bar.add_cascade(label="Debug", menu=self.menu_debug)

        # Attach menu bar to the root window
        self.root.configure(menu=self.menu_bar)

        # Table Selection List
        self.listbox_tables = tk.Listbox(self.root, width=30)
        self.listbox_tables.pack(side="left", fill="y", expand=False)
    
        # Info Pane on the Right
        self.app_info = ttk.Frame(self.root)
        self.app_info.pack(fill="both", expand=True)

        # Info Pane Label
        self.lbl_curr_table = ttk.Label(self.app_info, 
            text="", 
            justify="center", anchor="center")
        self.lbl_curr_table.pack(side="top", fill="both")

        # Info Pane Tabs
        self.app_tabs = ttk.Notebook(self.app_info)
        self.app_tabs.pack(fill=tk.BOTH, expand=True)

        self.tab_table = ttk.Frame(self.app_tabs)
        self.tab_results = ttk.Frame(self.app_tabs)
        self.app_tabs.add(self.tab_table, text=f"{'Table Info':^20}")
        self.app_tabs.add(self.tab_results, text=f"{'Roll Results':^20}")
    
        # Table Info Tab
        self.tree_curr_table = ttk.Treeview(self.tab_table, columns=("Roll",
            "Results"))
        self.tree_curr_table.column("#0", width=0, stretch=False)
        self.tree_curr_table.column("Roll", width=50, stretch=False)
        self.tree_curr_table.column("Results")

        self.tree_curr_table.heading("Roll", text="Roll")
        self.tree_curr_table.heading("Results", text="Results")

        self.tree_curr_table.pack(fill=tk.BOTH, expand=True)

        # Roll Results Tab
        self.text_res = tk.Text(self.tab_results, wrap="word")
        self.btn_roll = tk.Button(self.tab_results, text="Roll New Result",
            command=self.addResult)
        self.text_res.pack(side="top", expand=True, fill="both")
        self.btn_roll.pack(side="bottom", fill="x")
        # Make the text box read only and un editable
        self.text_res.config(state="disabled")

        # Event Binds
        self.listbox_tables.bind("<<ListboxSelect>>", self.eventTableSelection)

    def doNothing(self) -> None:
        ''' Placeholder that does nothing '''
        pass

    def exitApplication(self) -> None:
        ''' Destory the window and exit the app '''
        self.root.destroy()

    def menuDebugPrintFiles(self) -> None:
        ''' Print file names to console '''
        print(self.app_loaded_files)

    def menuDebugPrintTables(self) -> None:
        ''' Print loaded tables to console, lots of output '''
        print(self.app_loaded_tables)

    def menuDebugPrintSelectedTable(self) -> None:
        ''' print only the currently selected table '''
        self.app_current_table_info = self.app_loaded_tables[
            self.app_selected_table]
        print(self.app_current_table_info)

    def loadTablesFromFiles(self) -> None:
        ''' Load all table within the loaded yaml files. '''
        for file in self.app_loaded_files:
            with open(file, "r") as fobj:
                try:
                    tables = list(yaml.load_all(fobj, Loader=yaml.FullLoader))
                    for table in tables:
                        self.app_loaded_tables.append(Table(file, table))
                except Exception as e:
                    print(e)
        for table in self.app_loaded_tables:
            self.listbox_tables.insert(tk.END, table.getName())
                    
    def loadYamlFiles(self, dir=".\\tables\\*.yaml") -> None:
        ''' Get all file names in the given directory. '''
        all_files = glob.glob(dir)
        self.app_loaded_files = all_files

    def eventTableSelection(self, event) -> None:
        ''' Populate info pane table with selected table results '''
        selection = self.listbox_tables.curselection()        
        # Check if selection is different from previous selection
        if self.app_selected_table != self.app_loaded_tables[selection[0]]:
            # Set new selection
            self.app_selected_table = self.app_loaded_tables[selection[0]]
            # Remove items from selected table if they are different
            for item in self.tree_curr_table.get_children():
                self.tree_curr_table.delete(item)
            # Add currently selected table name.
            self.lbl_curr_table.configure(
                text=self.app_selected_table.getName()
            )
            # Add New items into the list.
            for res, val in self.app_selected_table.getAllResults().items():
                self.tree_curr_table.insert("", "end", values=(
                    res, val
                ))
    
    def addResultToLog(self, table:Table, key:int) -> None:
        """
        Given a table and a key, format a string to log the information to the 
        'text_res' Text widget.

        :param table: The table to get the result from.
        :param key: The key pair for the value in the table results dictionary.
        :return: None
        """
        msg = f"Rolled {key} on {table.getName()}:\n"
        msg += f"\t{result}\n"
        self.text_res['state'] = 'normal'
        self.text_res.insert('end lineend', msg)
        self.text_res['state'] = 'disabled'

    def rollOnTable(self, table:Table, rolls:int=1) -> int:
        """ 
        Given a table, and amount of rolls, roll on the table for results from
        the table.

        :param table: The table to 
        """
        roll = table.getRollNote()

        if roll == "length":
            roll = f"1d{len(table.getAllResults())}"
        
        if not isRollValid(roll):
            return -1

        for _ in range(rolls):
            face = rollDice()


    def findLinksInString(self, text:str) -> list[str]:
        """
        Given a string, find all substrincs incased within brackes and return
        them in a list.

        :param text: A string to be checked for encased brackets.
        :return: list of strings containing the parsed sub strings found within
            the main string.
        """ 
        brackets = []
        if "[" in text and "]" in text:
            subs = [i for i, ch in enumerate(text) if ch == "[" or ch == "]"]
        if brackets:
            links = []
            for i in range(0, len(brackets), 2):
                try:
                    links.append(text[brackets[i]:brackets[i+1]])
                except:
                    pass
        return links

    def parseTableLink(self, text:str) -> Dict[Literal['roll', 'table'], Optional[str]]:
        """
        Given a string, parse for a roll and table name with the formats:
            X@Z Where X is the amount of rolls on the table, and Z is the Table,
            - or - 
            XdY@Z where X is the amount of rolls, Y is the the max result per
            roll, and Z is the Table.

        :param text: string to be parsed.
        :return: dictionary containing necessary parsed data containing 'roll'
        for the roll amount to be evaluated. and 'table' if there 
        """ 
        res = {"roll": None, "table": None}
        s = text.split('@')
        if len(s) == 1:
            res['roll'] = s[0]
        elif len(s) >=2:
            res['roll'] = s[0]
            res['table'] = s[1]
        return res

    def run(self) -> None:
        ''' Run the application '''
        self.root.mainloop()

if __name__ == '__main__':
    app = TableRoller()