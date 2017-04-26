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
        self.container = None


    def add_widgets(self):
        """
            Adds and formats all of the
        """
        self.child_items['start_frame'] = tk.LabelFrame(self.parent, text='Start a container')
        self.child_items['start_frame'].pack(fill='both', expand='yes')

        # create the widgets to get the container name
        self.container_name = tk.StringVar()
        self.child_items['container_name_field'] = self.__create_text_field(
            self.child_items['start_frame'], self.container_name,
            'Container Name', self.create_container)[1]

        self.image_name = tk.StringVar()
        self.child_items['image_name_field'] = self.__create_text_field(
            self.child_items['start_frame'], self.image_name,
            'Image Name', self.create_container)[1]
        row_frame = tk.Frame(master=self.child_items["start_frame"])
        row_frame.pack()
        self.child_items['port_fields'] = PortWidget(row_frame)
        self.child_items['port_fields'].pack()
        tk.Button(master=self.child_items['start_frame'], text="Start/Stop",
                  command=self.create_container).pack(side=tk.BOTTOM)
    def create_container(self):
        '''
            Creates a container
        '''
        if not self.container:
            client = docker.from_env()
            self.container = client.containers.run(image=self.image_name.get(),
                                                   hostname=self.container_name.get(),
                                                   name=self.container_name.get(),
                                                   ports=self.child_items['port_fields'].get_dict())
        else:
            self.container.kill()
            self.container = None

    def __create_text_field(self, parent, variable, label_txt, on_enter):
        '''
        Returns a tuple with a Frame and a label, text field pair
        based on the parameters passed. And packs it into

        parent = the parent frame
        variable = variable that the Entry/text field should represent
        label_txt = the txt for the label
        onEnter = the function to call when enter is pressed in the entry field
        '''
        temp_frame = tk.Frame(parent)
        temp_label = tk.Label(temp_frame, text=label_txt)
        temp_field = tk.Entry(temp_frame, textvariable=variable)
        temp_field.bind('<Return>', on_enter)
        temp_frame.pack()
        temp_label.pack(side=tk.LEFT)
        temp_field.pack(side=tk.RIGHT)
        return (temp_frame, (temp_label, temp_label))

class PortWidget(tk.LabelFrame):
    '''
    Represents a table of Guest/host ports
    '''
    def __init__(self, parent):
        super().__init__(master=parent, text="Ports")
        # set up the list for the ports
        self.guest_ports = []
        self.host_ports = []
        self.protocols = []

        self.add_button = tk.Button(master=self, text="Add Port Pair", command=self.add_row)
        self.add_button.grid(row=0, column=1, padx=10, pady=10)
        self.button_pressed = False # flag
        self.add_button = tk.Button(master=self, text="Test dict", command=self.get_dict)
        self.add_button.grid(row=0, column=2, padx=10, pady=10)

    def add_row(self):
        '''
            Adds another row to the widget(offering another guest/host pair)
        '''
        if not self.button_pressed:
            # add the column headers
            header = tk.Label(master=self, text='Host')
            header.grid(row=1, column=0)
            header = tk.Label(master=self, text='Protocol')
            header.grid(row=1, column=1)
            header = tk.Label(master=self, text='Guest')
            header.grid(row=1, column=2)
            self.button_pressed = True

        row = len(self.guest_ports) + 2 # the row that we need to add to

        # create the string vars add add them to there respective lists
        host = tk.StringVar()
        protocol = tk.StringVar()
        guest = tk.StringVar()
        self.host_ports.append(host)
        self.guest_ports.append(guest)
        self.protocols.append(protocol)

        # create the inputs
        tk.Entry(master=self, textvariable=host).grid(row=row, column=0, padx=10, pady=10)
        tk.Entry(master=self, textvariable=protocol).grid(row=row, column=1, padx=10, pady=10)
        tk.Entry(master=self, textvariable=guest).grid(row=row, column=2, padx=10, pady=10)

    def get_dict(self):
        '''
            returns the dict of ports
        '''
        port_map = {}
        for i in range(len(self.host_ports)):
            host_port = self.host_ports[i].get()
            protocol = self.protocols[i].get()
            guest_port = self.guest_ports[i].get()

            # check data and correct if necessary
            if guest_port == '': # skip if guest port is blank
                continue
            if protocol == '':
                protocol = 'tcp'
            if host_port == '':
                host_port = None

            port_map[guest_port + '/' + protocol] = host_port

        return port_map

root = tk.Tk()
app = Application(parent=root)
app.mainloop()

