import tkinter as tk
from tkinter import ttk

def create_tab_content(tab):
    """ Create a Label widget with instructions for each tab. """
    label = tk.Label(tab, text=f"This is {tab} content.")
    label.pack(padx=10, pady=10)

root = tk.Tk()
root.title("Notebook Example")

# Create a Notebook widget
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Create the first tab
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Tab 1")
create_tab_content(tab1)

# Create the second tab
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Tab 2")
create_tab_content(tab2)

# Create the third tab
tab3 = ttk.Frame(notebook)


root.mainloop()