from tkinter import *
from tkinter import messagebox
import sys

class VM(Frame):
    #initalizes the VM
    def __init__(self, master=None):
        print("VM: Assembling")
        Frame.__init__(self, master)
        self.nul = None
        self.master = master
        self.init_window()
        self.master.configure(background='black')
        self.lines = []
        self.instructions = {
            b'\x01': self.print,
            b'\x02': self.move,
            b'\x03': self.nul,
            b'\x04': self.nul,
            b'\x05': self.nul,
            b'\x06': self.nul,
            b'\x08': self.nul,
            b'\x09': self.nul,
            b'\x0a': self.nul,
            b'\x0b': self.nul,
            b'\x0c': self.nul,
            b'\x0d': self.nul,
            b'\x0e': self.nul,
            b'\x0f': self.nul,
            b'\x10': self.nul,
            b'\x11': self.nul,
            b'\x12': self.nul,
            b'\x13': self.nul,
            b'\x14': self.nul,
            b'\x15': self.nul,
            b'\x16': self.nul,
            b'\x17': self.nul,
            b'\x18': self.nul,
            b'\x19': self.nul,
            b'\x1a': self.nul,
            b'\x1b': self.nul
        }
        self.registers = {
            'a': [None, None],
            'b': [None, None],
            'c': [None, None],
            'd': [None, None],
            'e': [None, None],
            'f': [None, None],
            'g': [None, None],
            'h': [None, None],
            'i': [None, None],
            'j': [None, None], #for jumping
            'k': [None, None],
            'l': [None, None],
            'm': [None, None],
            'n': [None, None],
            'o': [None, None],
            'p': [None, None], #for printing
            'q': [None, None],
            'r': [None, None],
            's': [None, None],
            't': [None, None],
            'u': [None, None],
            'v': [None, None],
            'w': [None, None],
            'x': [None, None],
            'y': [None, None],
            'z': [None, None],
        }
        self.stack = []
        
        self.varibles = {}
        self.sections = {}
        print("VM: Assembled")

    #configues window
    def init_window(self):
        self.master.title("Fox VM RunTime")
        self.configure(background='black')
        self.pack(fill=BOTH, expand=True)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)
        menu.configure(background='black')
        menu.configure(foreground='white')

    #shuts down the window
    def client_exit(self):
        self.delete()
        exit()
    #deletes major parts of the VM
    def delete(self):
        print("VM: Disassembing")
        del self.lines
        del self.master
        del self.instructions
        del self.registers
        del self.stack
        del self.varibles
        del self.sections
        print("VM: Disassembed")
        
    #print to window (1) (first instruction)
    def print(self):
        self.lines.append(Label(self, text=str(self.registers["p"][0]), fg="white", bg="black"))
        self.lines[-1].pack(anchor='w', side= TOP)
    #makes a varible (2)
    def make(self, variable):
        self.varibles[variable.decode()] = None
    #move value to varible at top of stack (3)
    def move(self, value):
        type_ = value[-1]
        if type_ == b'\xe1':
            value = int(value[0:len(value)-1])
        if type_ == b'\xe2':
            value = str(value[0:len(value)-1].decode())
        if type_ == b'\xe3':
            value = float(value[0:len(value)-1])
        self.varibles[self.stack[0]] = value
    #loads a variable to top of stack (4)
    def load(self, variable):
        variable = vaiable.decode()
        if variable in self.stack:
            self.stack.pop(self.stack.index(variable))
        self.stack.insert(0, varible)
    #unloads a varible from the stack (5)
    def unload(self, variable):
        variable = vaiable.decode()
        if variable not in self.stack:
            pass
        self.stack.pop(self.stack.index(variable))
    #sets register value of variable in top of stack (6)
    def set_register(self, register):
        self.registers[str(register[0].decode())][int(register[1])] = self.varibles[self.stack[0]] 
    #read register to the variable at the top of stack (7)
    def read_register(self, register):
        self.varibles[self.stack[0]] = self.registers[str(register[0].decode())][int(register[1])]
    


root = Tk()
root.geometry("400x300")
app = VM(root)
app.print()
root.protocol("WM_DELETE_WINDOW", root.iconify)
root.mainloop()