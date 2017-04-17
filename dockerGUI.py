#! /bin/python
"""
This file hosts the GUI aspects of the project.
"""
# Tries to import docker, otherwise will try to resolve the dependancy
try:
    import docker
except ModuleNotFoundError:
    print("The docker module was not found. Would you like to install it?")
    answer = input("[Y/n] >")
    if answer[0].lower() == 'n':
        print("The program cannot operate without docker and will now exit.")
        exit()
    else:
        import pip
        pip.main(['install', 'docker'])

import tkinter as tk
# Class definitions
class TextField(tk.Frame):
    def __init__(self, parent, variable, labelText=None, onEnter=None):
        super().__init__(master=parent)
        if labelText:
            self.label = tk.Label(parent, text=labelText)
            self.label.pack(side=tk.LEFT)
        if onEnter:
            self.field = tk.Entry(parent, textvariable=variable)
            self.field.bind("<Return>", onEnter)
        else:
            self.field = tk.Entry(parent)
        self.field.pack(side=tk.RIGHT)

class Application(tk.Frame):
    """
        Manages the overall GUI aspects of the program as well as
        the calls to the docker api
    """

    def __init__(self, parent=None):
        super().__init__(master=parent)
        self.pack()
        self.child_items = {}
        self.add_widgets()


    def add_widgets(self):
        """
            Adds and formats all of the
        """
        self.curr_container_name = tk.StringVar()
        self.child_items['containerNameField'] = TextField(self, variable=self.curr_container_name,
                                                           labelText="Name", onEnter=self.hello)
        self.child_items['containerNameField'].pack()

    def hello(self, *args):
        print(self.curr_container_name.get())

root = tk.Tk()
app = Application(parent=root)
app.mainloop()

