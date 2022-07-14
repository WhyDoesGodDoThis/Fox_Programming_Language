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
            b'\x02': self.make,
            b'\x03': self.move,
            b'\x04': self.load,
            b'\x05': self.unload,
            b'\x06': self.set_register,
            b'\x07': self.read_register,
            b'\x08': self.new_section,
            b'\x09': self.jump,
            b'\x0a': self.jump_equal,
            b'\x0b': self.jump_notequal,
            b'\x0c': self.jump_less,
            b'\x0d': self.jump_greater,
            b'\x0e': self.jump_lessor,
            b'\x0f': self.jump_greateror,
            b'\x10': self.cycleStack,
            b'\x11': self.nul,
            b'\x12': self.nul,
            b'\x13': self.nul,
            b'\x14': self.nul,
            b'\x15': self.nul,
            b'\x16': self.nul,
            b'\x17': self.nul,
            b'\x18': self.nul,
            b'\x19': self.nul,
            b'\x1a': self.nul
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
        self.linepointer = 0
        self.runtime = False
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
        menu.add_cascade(label="Options", menu=file)
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
        
    #print to window (1)
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
    #addes a new section to sections (8)
    def new_section(self, sectionName, line):
        self.sections[str(sectionName.decode())] = line
    #jump to given section (9)
    def jump(self, section):
        self.linepointer = self.sections[str(section.decode())]
    #jump to given section if j registers are equal (10)
    def jump_equal(self, section):
        if self.registers['j'][0] == self.registers['j'][1]:
            self.linepointer = self.sections[str(section.decode())]
    #jump to given section if j registers are not equal (11)
    def jump_notequal(self, section):
        if self.registers['j'][0] != self.registers['j'][1]:
            self.linepointer = self.sections[str(section.decode())]
    #jump to given section if j registers are less (12)
    def jump_less(self, section):
        if self.registers['j'][0] < self.registers['j'][1]:
            self.linepointer = self.sections[str(section.decode())]
    #jump to given section if j registers are greter (13)
    def jump_greater(self, section):
        if self.registers['j'][0] > self.registers['j'][1]:
            self.linepointer = self.sections[str(section.decode())]
    #jump to given section if j registers are less or equal (14)
    def jump_lessor(self, section):
        if self.registers['j'][0] <= self.registers['j'][1]:
            self.linepointer = self.sections[str(section.decode())]
    #jump to given section if j registers are greter or equal (15)
    def jump_greateror(self, section):
        if self.registers['j'][0] >= self.registers['j'][1]:
            self.linepointer = self.sections[str(section.decode())]
    #cycles first item in stack to the back of the stack (16)
    def cycleStack(self):
        self.stack.append(self.stack.pop(0))
    #Main RunTime
    def Runtime(self, code_list):
        print("PreRunTimeChecker: Starting")
        for index, line in enumerate(code_list):
            if line[0] == b'\x08':
                if line[1:] == b'S':
                    self.runtime = True
                    self.new_section("S", index+1)
                    continue
                self.new_section(line[1:], index)
        print("PreRunTimeChecker: Finished")
def Main():
    root = Tk()
    root.geometry("400x300")
    app = VM(root)
    app.print()
    root.protocol("WM_DELETE_WINDOW", root.iconify)
    root.mainloop()
    
if __name__ == "__main__":
    Main()