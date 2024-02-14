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

class TableRoller():
    def __init__(self) -> None:
        ''' Initialize the app '''
        # instance variables
        self.debug = True
        self.app_loaded_files = []
        self.app_loaded_tables = []
        self.app_selected_table = -1

        self.initWindow()
        self.loadYamlFiles()
        self.loadTablesFromFiles()

        self.run()

    def initWindow(self) -> None:
        ''' Initialize app window, load and configure widgets, load configs '''
        self.root = tk.Tk()
        self.root.title("Tribbs' Table Roller")
        self.root.geometry("800x600")
        self.root.iconbitmap("./assets/py-app-icon.ico")

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

        # Table Info Pane
        self.info_pane = tk.Frame(self.root)
        self.info_pane.pack(side="right", fill=tk.BOTH, expand=True)

        # Info Pane Label
        self.info_pane_label = tk.Label(self.info_pane, text="", height=1)
        self.info_pane_label.pack(fill="x", expand=False)
        
        # Info Pane Table
        self.info_pane_table = ttk.Treeview(
            self.info_pane,
            columns=("result", "desc"),
            show="headings",
            selectmode="browse"    
        )
        self.info_pane_table.heading("result", text="Result")
        self.info_pane_table.heading("desc", text="Description")
        self.info_pane_table.column("result", width=2)
        self.info_pane_table.pack(fill=tk.BOTH, expand=True)

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
        pass

    def loadTablesFromFiles(self) -> None:
        ''' Load all tables within the loaded yaml files.  '''
        for file in self.app_loaded_files:
            with open(file, 'r') as f:
                data = list(yaml.load_all(f, Loader=yaml.FullLoader))
                for table in data:
                    self.app_loaded_tables.append(table)
        ''' Add All tables names to the tables listbox '''
        for table in self.app_loaded_tables:
            if 'name' in table:
                self.listbox_tables.insert(tk.END, table['name'])
            if 'table-name' in table:
                self.listbox_tables.insert(tk.END, table['table-name'])

    def loadYamlFiles(self, dir=".\\tables\\*.yaml") -> None:
        ''' Get all file names in the given directory. '''
        all_files = glob.glob(dir)
        self.app_loaded_files = all_files

    def eventTableSelection(self, event) -> None:
        ''' Populate info pane table with selected table results '''
        selection = self.listbox_tables.curselection()
        self.app_selected_table = selection
        self.info_pane_label.configure(text=self.listbox_tables.get(selection))

    def run(self) -> None:
        ''' Run the application '''
        self.root.mainloop()

if __name__ == '__main__':
    app = TableRoller()
