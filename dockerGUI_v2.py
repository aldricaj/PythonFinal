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

BOX_WIDTH = 2

class Application(tk.Frame):
    """
        Manages the overall GUI aspects of the program as well as
        the calls to the docker api
    """

    def __init__(self, parent=None):
        super().__init__(master=parent)
        # a dictionary of items
        # any label, field pairs are stored in a tuple with
        # label as [0] and field as [1]
        self.child_items = {}

        self.parent = parent
        self.pack()

        self.add_widgets()


    def add_widgets(self):
        """
            Adds and formats all of the
        """
        self.child_items['start_frame'] = tk.LabelFrame(self.parent, text='Start a container')
        self.child_items['start_frame'].pack(fill='both', expand='yes')

        # create the widgets to get the container name
        self.container_name = tk.StringVar()
        temp_frame = tk.Frame(self.child_items['start_frame'])
        temp_label = tk.Label(temp_frame, text='Container Name')
        temp_field = tk.Entry(temp_frame, textvariable=self.container_name)
        temp_field.bind('<Return>', self.create_container)
        temp_frame.pack()
        temp_label.pack(side=tk.LEFT)
        temp_field.pack(side=tk.RIGHT)
        self.child_items['container_name_field'] = (temp_label, temp_field)

        temp_frame = tk.Frame(self.child_items['start_frame'])
        temp_label = tk.Label(temp_frame, text='Container N3ame')
        temp_field = tk.Entry(temp_frame, textvariable=self.container_name)
        temp_field.bind('<Return>', self.create_container)
        temp_frame.pack()
        temp_label.pack(side=tk.LEFT)
        temp_field.pack(side=tk.RIGHT)

    def create_container(self):
        '''
            Creates a container
        '''
        pass
    def __create_TextField(self, parent, variable, name, onEnter):
        pass
root = tk.Tk()
app = Application(parent=root)
app.mainloop()

