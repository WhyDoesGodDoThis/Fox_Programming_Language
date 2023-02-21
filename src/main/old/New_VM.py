from tkinter import *
import struct

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
            1: self.print,
            2: self.make,
            3: self.move,
            4: self.load,
            5: self.unload,
            6: self.set_register,
            7: self.read_register,
            8: self.new_section,
            9: self.jump,
            10: self.jump_equal,
            11: self.jump_notequal,
            12: self.jump_less,
            13: self.jump_greater,
            14: self.jump_lessor,
            15: self.jump_greateror,
            16: self.cycleStack,
            17: self.nul,
            18: self.nul,
            19: self.nul,
            20: self.nul,
            21: self.nul,
            22: self.nul,
            23: self.nul,
            24: self.nul,
            25: self.nul,
            26: self.nul
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
        self.varibles[str(variable.decode())] = None
    #move value to varible at top of stack (3)
    def move(self, value):
        type_ = value[-1]
        for i in (225, 226, 227):
            try:
                value.pop(value.index(i))
            except ValueError:
                pass
        if type_ == 225:
            value = int.from_bytes(value, "big")
        if type_ == 226:
            value = value.decode()
        if type_ == 227:
            value = float(struct.unpack('>f', bytes(value)))
        self.varibles[self.stack[0]] = value
    #loads a variable to top of stack (4)
    def load(self, variable):
        variable = variable.decode()
        if variable in self.stack:
            self.stack.pop(self.stack.index(variable))
        self.stack.insert(0, variable)
    #unloads a varible from the stack (5)
    def unload(self, variable):
        variable = variable.decode()
        if variable not in self.stack:
            pass
        self.stack.pop(self.stack.index(variable))
    #sets register value of variable in top of stack (6)
    def set_register(self, register):
        self.registers[chr(register[0])][int(register[1])] = self.varibles[self.stack[0]] 
    #read register to the variable at the top of stack (7)
    def read_register(self, register):
        self.varibles[self.stack[0]] = self.registers[chr(register[0])][int(register[1])]
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
            if int(line[0]) == 8:
                if line[1:] == b'S':
                    self.runtime = True
                    self.new_section(b"S", index+1)
                    continue
                self.new_section(line[1:], index)
        if not self.runtime:
            print("PreRunTimeChecker Error: ee")
            self.client_exit()
        print("PreRunTimeChecker: Finished")
        print("Runtime: Starting")
        while self.runtime:
            tline = code_list[self.linepointer]
            instr = int(tline[0])
            if instr in (16, 1):
                self.instructions[tline[0]]()
                self.linepointer += 1
                continue
            if instr == 8:
                self.linepointer += 1
                continue
            if instr in (2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15):
                self.instructions[tline[0]](tline[1:len(tline)])
                self.linepointer += 1
                continue
            if instr == 254:
                print("Runtime: Finished")
                self.runtime = False

def Main():
    root = Tk()
    root.geometry("500x375")
    app = VM(root)
    app.Runtime(bytearray(open("a", 'rb').read()).split(b'\xff'))
    root.protocol("WM_DELETE_WINDOW", root.iconify)
    root.mainloop()
    
if __name__ == "__main__":
    Main()