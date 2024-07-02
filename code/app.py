import tkinter as tk
import tkinter.font as tkFont
import tkinter.scrolledtext as ScrolledText
from tkinter import ttk
from tkinter import filedialog
import models as m
import file_handler as fh
import os
import random

class TableRollerApp():
    def __init__(self, debug:bool=False) -> None:
        random.seed()
        self.curr_table = None

        self.debug = debug
        self.win_size_w = 800
        self.win_size_h = 500

        # ROOT WINDOW CONFIGURATION
        self.root = tk.Tk()
        self.root.title("TTRPG Tools: Table Roller")
        self.root.geometry(f"{self.win_size_w}x{self.win_size_h}")
        self.font = tkFont.Font(family="Ubuntu Mono", size=10,
            weight=tkFont.NORMAL)

        self.file_handler = fh.FileHandler(os.path.dirname(
            os.path.realpath(__file__)))
        self.resolver = m.Resolver()

        self.initWidgets()

        self.list_tables.bind("<ButtonRelease-1>", self.onTableSelection)

    def initWidgets(self) -> None:
        # MENUS
        self.menu_bar = tk.Menu()
        # File Menu Cascade
        self.menu_file = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_file.add_command(label="Load File",
            command=self.loadFromFile)
        self.menu_file.add_command(label="Load Folder",
            command=self.loadFromDir)
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Exit", command=self.exitApp)
        self.menu_bar.add_cascade(label="File", menu=self.menu_file)
        # Attach menu bar
        self.root.configure(menu=self.menu_bar)
        # Settings Menu Cascade
        self.menu_tools = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_tools.add_command(label="Clear Rolls",
            command=self.clearTextRolls)
        self.menu_tools.add_command(label="Clear Errors",
            command=self.clearTextLogs)
        self.menu_bar.add_cascade(label="Tools", menu=self.menu_tools)

        # TABLE LIST
        self.list_tables = tk.Listbox(self.root)
        self.list_tables.grid(column=0, row=0, rowspan=2,
            sticky=(tk.N, tk.E, tk.S, tk.W), padx=2, pady=2)
        self.list_tables.insert(0, "Table List")
        
        # NOTEBOOK WIDGET
        self.tabs = ttk.Notebook(self.root)
        self.tabs.grid(column=1, row=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        #self.tabs.configure(font=self.font)

        # ROLL BUTTON
        self.button_roll = tk.Button(self.root, text="Roll",
            command=self.onButtonRoll)
        self.button_roll.grid(column=1, row=1, sticky=(tk.N, tk.E, tk.S, tk.W), 
            padx=2, pady=2)

        # TAB -> RESULTS
        self.tabs_results = tk.Frame(bg="red")
        self.listbox_results = tk.Listbox(self.tabs_results)
        self.listbox_results.grid(column=1, row=1,
            sticky=(tk.N, tk.E, tk.S, tk.W))
        self.listbox_results.configure(font=self.font)
        self.listbox_results.insert(0, "Results For Selected Table")
        self.listbox_results.pack(fill=tk.BOTH, expand=1)
        self.tabs.add(self.tabs_results, text=f"{'Results':^15}")

        # TAB -> ROLLS
        self.tabs_roll = tk.Frame()
        self.tabs.add(self.tabs_roll, text=f"{'Rolls Logs':^15}")
        self.text_rolls = tk.Text(self.tabs_roll)
        self.text_rolls.pack(fill=tk.BOTH, expand=1, padx=2, pady=2)
        self.text_rolls.configure(font=self.font, wrap=tk.WORD)
        self.text_rolls.config(state=tk.DISABLED)
        yscroll = tk.Scrollbar()

        # TAB -> LOGS
        self.tabs_logs = tk.Frame()
        self.tabs.add(self.tabs_logs, text=f"{'Error Logs':^15}")
        self.text_logs = tk.Text(self.tabs_logs)
        self.text_logs.pack(fill=tk.BOTH, expand=1, padx=2, pady=2)
        self.text_logs.configure(font=self.font, wrap=tk.WORD)
        #self.text_logs.insert("1.0", "Text Bot for Debug/Error Logs")
        self.text_logs.config(state=tk.DISABLED)

        # ROW & COLUMN CONFIGURATION 
        self.root.columnconfigure(0, weight=2)
        self.root.columnconfigure(1, weight=3)
        self.root.rowconfigure(0, weight=1)

    def loadFromFile(self) -> None:
        file = filedialog.askopenfile("r", title="Choose File...",
            initialdir=self.file_handler.dir, filetypes=(
            ("YAML", "*.yaml *.yml"), ("Text Files", "*.txt"),
            ("JSON", "*.json")))
        if file:
            loaded = self.file_handler.loadFile(file.name)
            self.resolver.update(self.tableConstruction(loaded))
            self.checkForProblems()
            self.updateTableList()

    def loadFromDir(self) -> None:
        dir = filedialog.askdirectory(title="Choose Folder...",
            initialdir=self.file_handler.dir)
        if dir:
            blob = self.file_handler.loadFiles(dir)
            loaded = self.file_handler.loadFiles(dir)
            tables = {}
            for dicts in loaded:
                new_Tabels = self.tableConstruction(dicts)
                for name, table in new_Tabels.items():
                    if name not in tables:
                        tables[name] = table
                    else:
                        self.updateTextLogs(
                            f"TABLE {name} already in loaded tables."
                        )
            self.resolver.update(tables)
            self.checkForProblems()
            self.updateTableList()

    def tableConstruction(self, data) -> dict:
        new_dict = {}
        for k, v in data.items():
            throw_away = m.Table()
            new_dict[k] = throw_away.create(v)
        return new_dict

    def onTableSelection(self, event):
        # get the widget
        widget = event.widget
        selection = widget.curselection()
        # get the item clicked in the list
        if selection:
            clicked = widget.get(selection)
            # send the name of the table to update Result Lists
            self.updateResultList(clicked)

    def onButtonRoll(self) -> None:
        """
        Event for Roll Button Clicked
        """
        if self.curr_table:
            roll = random.randint(1, self.curr_table.length)
            result = self.curr_table.getResult(roll)
            if result:
                msg = f"On {self.curr_table.name} rolled {roll:<3}: "
                msg += f"\n  {self.resolver.get(result)}".replace('\t', ' > ')
                self.updateTextRolls(msg)
            else:
                msg = f"On {self.curr_table.name} rolled {roll:<3}: "
                msg += f"ERROR OCCURED, VALUE {roll} NOT FOUND ON TABLE"
                msg += f"{self.curr_table.name}."
                self.upateTextLogs(msg)
    
    def updateTableList(self) -> None:
        """
        Update the Table list when tables arte loaded from a file.
        """
        loaded_dict = self.resolver.tables
        # remove items currently in list
        self.list_tables.delete(0, self.list_tables.size()-1)
        # add items back into list
        for i, (name, table) in enumerate(loaded_dict.items()):
            self.list_tables.insert(i, name)

    def updateResultList(self, table_name) -> None:
        """
        Update the Result List for selected table.
        """
        table = self.resolver.tables[table_name]
        self.curr_table = None if not table else table
        # remove 
        if self.curr_table:
            self.listbox_results.delete(0, self.listbox_results.size())
            # add items to the result list
            for i in range(table.length):
                self.listbox_results.insert(i, 
                    f"{i+1:>3}: {table.getRawResult(i+1)}")
        
    def updateTextRolls(self, text:str) -> None:
        """
        Update the text within self.text_rolls
        :param text: str. Text to be added to the text box.
        """
        self.text_rolls.config(state=tk.NORMAL)
        utext = self.text_rolls.get("1.0", "end")
        self.text_rolls.delete("1.0", "end")
        self.text_rolls.insert("1.0", f"{utext}{text}")
        self.text_rolls.config(state=tk.DISABLED)

    def updateTextLogs(self, text:str) -> None:
        """
        Update the text within self.text_logs
        :param text: str. Text to be added to the text box.
        """
        self.text_logs.config(state=tk.NORMAL)
        utext = self.text_logs.get("1.0", "end")
        self.text_logs.delete("1.0", "end")
        self.text_logs.insert("1.0", f"{utext}{text}")
        self.text_logs.config(state=tk.DISABLED)

    def clearTextLogs(self) -> None:
        self.text_logs.config(state=tk.NORMAL)
        self.text_logs.delete("1.0", "end")
        self.text_logs.config(state=tk.DISABLED)

    def clearTextRolls(self) -> None:
        self.text_rolls.config(state=tk.NORMAL)
        self.text_rolls.delete("1.0", "end")
        self.text_rolls.config(state=tk.DISABLED)

    def checkForProblems(self) -> None:
        """
        Called to check for and log any issues with tables. Output issues to Log
        textbox.
        """
        tables = self.resolver.tables
        # Tables check
        for table in tables:
            if not tables[table]:
                self.updateTextLogs(f">> Table '{table}' not loaded properly.")
                continue
            for i in range(1, tables[table].length+1):
                # Results range check
                if i not in tables[table].results:
                    msg = f">> Roll {i} not found in {tables[table].name}"
                    self.updateTextLogs(msg)
                    continue
                # Result Object check
                if not tables[table].results[i]:
                    msg = f">> Result for roll {i} in {tables[table].name} not"
                    msg += " found."
                    self.updateTextLogs(msg)
                    continue
                #Check that linked tables exist wihint loaded tables.
                links = tables[table].results[i].links
                if links:
                    for link in links:
                        if links[link]:
                            if (links[link].table
                            and not links[link].table in tables.keys()): 
                                msg = f">> Linked roll '{links[link].table}'"
                                msg += f" not found in '{tables[table].name}'"
                                msg += f" result {i}."
                                self.updateTextLogs(msg)
                                continue

    def doNothing(self) -> None:
        """
        This code does nothing. Place holder function.
        """
        pass

    def runApp(self):
        """
        Run the application by calling the tkinter mainloop
        """
        self.root.mainloop()

    def exitApp(self) -> None:
        """
        Close the window and exit the app.
        """
        self.root.destroy()

if __name__ == "__main__":
    app = TableRollerApp()
    app.runApp()