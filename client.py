from tkinter import *
import tkinter.scrolledtext as tkst
import socket
import threading

Host = 'localhost'
Port = 25565

class Application(Frame):
    def NewOutput(self, Output):
        self.Terminal.insert(INSERT, (Output + '\n'))
        self.Terminal.see(END)

    def NewInput(self, event):
        if self.GetInput == True:
            self.LastInput = str(self.Input.get())
        self.Input.delete(0,END)

    def createWidgets(self):
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.Terminal = tkst.ScrolledText(self)
        self.Terminal.grid(row=0, column=0, sticky=N+S+E+W)

        self.Input = Entry(self)
        self.Input.bind('<Return>', self.NewInput)
        self.Input.grid(row=1, column=0, sticky=N+S+E+W)


    def RecieveOutput(self):
        while True:
            Recieved = self.Messager.recv(1024)
            self.NewOutput(Recieved.decode())

    def MainThread(self):
        # First get Connected,
        self.NewOutput("Looking for a connection")
        global Host
        global Port
        FailedConnections = 0
        while True:
            try:
                self.Messager.connect((Host, Port))
                self.NewOutput("We Connected with " + str(FailedConnections) + " Failed Connections")
                break
            except ConnectionRefusedError:
                FailedConnections = FailedConnections + 1

        self.GetInput = True
        self.NewOutput("Please enter your username: ")
        while True:
            if self.LastInput != None:
                self.Username = self.LastInput
                self.GetInput = False
                self.LastInput = None

                self.NewOutput("Your username is: " + str(self.Username))
                self.Messager.send(str.encode(self.Username))
                break

        RecieveThread = threading.Thread(target=self.RecieveOutput)
        RecieveThread.start()

        self.GetInput = True
        while True:
            if self.LastInput != None:
                self.NewOutput(self.Username + ": " + self.LastInput)
                self.Messager.send(str.encode(self.Username + ": " + self.LastInput))
                self.LastInput = None

    def InitThread(self):
        SocketThread = threading.Thread(target=self.MainThread)
        SocketThread.start()

    def __init__(self, master=None):
        self.LastInput = None
        self.GetInput = False
        self.Messager = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        Frame.__init__(self, master)
        #self.pack()
        self.grid(sticky=N+S+E+W)
        self.createWidgets()

root = Tk()

app = Application(master=root)
app.after(500, app.InitThread)
app.mainloop()

root.destroy()