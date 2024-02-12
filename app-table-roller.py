'''
    Name: 
        Tribbs' Table Roller
    Desc: 
        Loads in formatter YAML files from specified folder and allows user to
    select loaded tables and roll on them. Should be able to also roll linked 
    tables from the loaded table if applicable. 
'''
import tkinter as tk
import yaml
import glob

def app() -> None:
    # Application functions
    def doNothing() -> None:
        ''' Placeholder that does nothing '''
        pass

    def exitApplication() -> None:
        ''' Destroy main window and exit application '''
        root.destroy()

    def menuDebugPrintFiles() -> None:
        for each in app_loaded_files:
            print(each)

    def menuDebugPrintTables() -> None:
        for table in app_loaded_tables:
            if 'name' in table:
                print(table['name'])
            if 'table-name' in table:
                print(table['table-name'])

    def loadYamlFiles(dir=None) -> list:
        ''' Get all file names in the given directory '''
        if dir != None:
            pass
        else:
            path = ".\\tables\\*.yaml"
            all_files = glob.glob(path)
            return all_files

    def loadTablesFromFiles() -> None:
        for file in app_loaded_files:
            with open(file, 'r') as f:
                data = list(yaml.load_all(f, Loader=yaml.FullLoader))
                for each in data:
                    app_loaded_tables.append(each)

    def loadTableListbox() -> None:
        for table in app_loaded_tables:
            if 'name' in table:
                listbox_tables.insert(tk.END, table['name'])
            if 'table-name' in table:
                listbox_tables.insert(tk.END, table['table-name'])

    # Application variables
    app_loaded_files = []
    app_loaded_tables = []

    # Main Window
    root = tk.Tk()
    root.title("Tribbs' Table Roller")
    root.geometry("800x600")
    root.iconbitmap("./assets/py-app-icon.ico")

    # Menu Bar
    menu_bar = tk.Menu()

    # Create A File Menu
    menu_file = tk.Menu(menu_bar, tearoff=0)
    menu_file.add_command(label="Reload Tables", command=doNothing)
    menu_file.add_command(label="Load Tables From...", command=doNothing)
    menu_file.add_separator()
    menu_file.add_command(label="Exit", command=exitApplication)
    menu_bar.add_cascade(label="File", menu=menu_file)

    # Debug Menu
    menu_debug = tk.Menu(menu_bar, tearoff=0)
    menu_debug.add_command(label="Print Loaded Files", 
        command=menuDebugPrintFiles)
    menu_debug.add_command(label="Print Loaded Tables", 
        command=menuDebugPrintTables)
    menu_bar.add_cascade(label="Debug", menu=menu_debug)

    # Table Selection List
    listbox_tables = tk.Listbox(root)
    listbox_tables.pack()

    # Attach menu bar to the main window
    root.config(menu=menu_bar)
    app_loaded_files = loadYamlFiles(None)
    loadTablesFromFiles()

    # Loadup functions
    loadTableListbox()

    # Start the main event loop
    root.mainloop()
    
if __name__ == "__main__":
    app()