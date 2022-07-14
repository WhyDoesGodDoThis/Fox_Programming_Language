import sys

#compiler to go with vm, this is the compiler for the vm
#this is the dictionary that converts the commands to numbers
convert = {
    "mov": 1,
    "pnt": 2,
    "frt": 3,
    "bck": 4,
    "add": 5,
    "sub": 6,
    "div": 7,
    "mlt": 8,
    "jmp": 10,
    "jif": 11,
    "jin": 12,
    "end": 255,
    "lbl": 9,
    "stk": 13,
    "cyl": 14,
    "crg": 15
}
#this is the compiler
def compiler(file_name):
    print("Compiler: Starting")
    #this is the list that will be returned
    out_code = []
    #this opens the file
    with open(file_name, 'r') as file:
        #this goes through each line
        for line in file:
            #this skips the line if it is a comment
            if line.startswith("#") or line.strip() == '' or line.strip().startswith('#'):
                continue
            #this removes the new line character
            line = line.strip()
            #this splits the line into a list
            line = line.split(' ')
            #this removes the comma from the second items in the list
            if len(line) > 1:
                line[1] = line[1].strip(",")
            if len(line) > 2:
                line[2] = line[2].strip(",")
            #this checks if the command is a label
            if line[0].count("_") == 0:
                #Unknown command error handling
                if line[0] not in convert:
                    print("Compiler Error: Invalid Command on line", len(out_code)+1)
                    sys.exit()
                #this converts the command to a number
                line[0] = convert[line[0]]
            else:
                #this adds the label to the list
                line.append(line[0][1:len(line[0])-1])
                #this sets the command to the label command
                line[0] = convert["lbl"]
            #this checks if the command is mov
            if line[0] == 1 and len(line) > 2:
                #this checks if the second item is a string
                if line[2].count('"') == 1:
                    #turns the list into a string
                    st = ''
                    for i in line[2:]:
                        i.replace('"', '')
                        st = st + str(i) + " "
                    line[2] = st
                #this checks if the second item is a number
                if line[2].isnumeric():
                    #this converts the second item to a number
                    line[1] = int(line[1])
            elif line[0] == 1 and len(line) < 3:
                print("Compiler Error: missing arguments for move instruction on line %d" % (len(out_code)+1))
                sys.exit()
            #check if the command is a clear register command
            if line[0] == 15 and len(line) > 1:
                if line[1] not in ('a','b','c','d', 'e', 'f', 'g', 'h'):
                    print("Compiler Error: no such register %s on line %d" % (line[1], len(out_code)+1))
                    sys.exit()
            elif line[0] == 15:
                print("Compiler Error: no register given on line %d" % (len(out_code)+1))
                sys.exit()
            #this adds the line to the list
            out_code.append(line)
    #this returns the list
    print("Compiler: Finished")
    return out_code

#class of the fox virtual machine with 12 instructions
class vm(object):
    def __init__(self):
        print("VM: Assembling")
        
        self.registers = {
            'a': [None, None],
            'b': [None, None],
            'c': [None, None],
            'd': [None, None],
            'e': [None, None],
            'f': [None, None],
            'g': [None, None],
            'h': [None, None],
        }
        
        self.instructions = {
            1: self.move,
            2: self.print,
            3: self.forward,
            4: self.backward,
            5: self.add,
            6: self.sub,
            7: self.div,
            8: self.mlt,
            9: self.sec,
            10: self.jmp,
            11: self.jmpif,
            12: self.jmpifnot,
            13: self.stk,
            14: self.cycle,
            15: self.clear_reg
        }
        
        self.stack = []
        self.dict = {}

        self.section = {}

        self.linepointer = 0
    
    #get value of given register
    def get_reg(self, reg):
        return self.registers[str(reg)[-2]][int(reg[-1])-1]
    #set register value
    def set_reg(self, reg, value):
        self.registers[str(reg)[-2]][int(reg[-1])-1] = value
    #undefined varible of Runtime error handling
    def stack_error(self, variable):
        #this checks if the variable is a register
        if "reg_" in variable:
            if variable[-1] in ('1','2'):
                if variable[-2] in ('a','b','c','d', 'e', 'f', 'g', 'h'):
                    return 0
        if variable not in self.stack:
            print("Runtime Error: Undefined variable %s on line %d" % (variable, self.linepointer+1))
            sys.exit()
    #undefined label of Runtime error handling
    def label_error(self, section):
        if section not in self.section:
            print("Runtime Error: Undefined label %s on line %d" % (section, self.linepointer+2))
            sys.exit()
    def register_error(self, register):
        if None in self.registers[register]:
            if self.registers[register][1] == None and None == self.registers[register][0]:
                errorreg = register
            else:
                errorreg = register + str(self.registers[register].index(None))
            print("Runtime Error: Null register %s on line %d" % (errorreg, self.linepointer+1))
    #move value to varible or register and put at bottom of stack (1) (move value, variable) (move 5, reg_a)
    def move(self, value, variable):
        if "reg_" in variable:
            self.set_reg(variable, value)
        else:
            if str(value) in self.dict:
                value = self.dict[str(value)] 
            if "reg_" in str(value):
                value = self.get_reg(value)
            if variable in self.stack:
                self.stack.pop(self.stack.index(variable))
            self.stack.append(variable)
            self.dict[str(variable)] = value
    #prints the value of variable (2) (print variable) (print reg_a)
    def print(self, variable):
        self.stack_error(variable)
        if "reg_" in variable:
            print(self.get_reg(variable))
        else:
            print(self.dict[str(variable)])
    #moves varible to the top of the stack (3) (forward variable) (forward reg_a)
    def forward(self, variable):
        self.stack_error(variable)
        self.stack.pop(self.stack.index(variable))
        self.stack.insert(0, str(variable))
    #moves variable to the bottom of the stack (4) (backward variable) (backward reg_a)
    def backward(self, variable):
        self.stack_error(variable)
        self.stack.pop(self.stack.index(variable))
        self.stack.insert(-1, str(variable))
    #adds reg_a and reg_b and assigns it to variable (5) (add variable) (add reg_a)
    def add(self, register, variable):
        self.register_error(register)
        self.move(int(self.registers[register][0]) + int(self.registers[register][1]), variable)
    #subtracts reg_a and reg_b and assigns it to variable (6) (sub variable) (sub reg_a)
    def sub(self, register, variable):
        self.register_error(register)
        self.move(int(self.registers[register][0]) - int(self.registers[register][1]), variable)
    #divides reg_a and reg_b and assigns it to variable (7) (div variable) (div reg_a)
    def div(self, register, variable):
        self.register_error(register)
        self.move(int(self.registers[register][0]) / int(self.registers[register][1]), variable)
    #multiply reg_a and reg_b and assigns it to variable (8) (mlt variable) (mlt reg_a)
    def mlt(self, register, variable):
        self.register_error(register)
        self.move(int(self.registers[register][0]) * int(self.registers[register][1]), variable)
    #declares a section to jump to (9) (sec name, linenum) (sec Start, 0)
    def sec(self, name, linenum):
        self.section[name] = linenum
    #jumps to section (10) (jmp section) (jmp Start)
    def jmp(self, section):
        self.label_error(section)
        if section in self.section:
            self.linepointer = self.section[section]
    #jumps to section if logic with reg_a and reg_b is True (11) (jmpif section, symbol) (jmpif Start, ==)
    def jmpif(self, register, section, symbol):
        self.label_error(section)
        if section in self.section:
            logic = eval(str(self.registers[register][0]) + str(symbol) + str(self.registers[register][1]))
            if logic:
                self.linepointer = self.section[section]
    #jumps to section if logic with reg_a and reg_b is False (12) (jmpifnot section, symbol)
    def jmpifnot(self, register, section, symbol):
        self.label_error(section)
        if section in self.section:
            logic = eval(str(self.registers[register][0]) + str(symbol) + str(self.registers[register][1]))
            if not logic:
                self.linepointer = self.section[section]
    #move top of the stack to varible (13)
    def stk(self, varible):
        self.move(self.stack[0], varible)
    #move first item in stack to back (14)
    def cycle(self):
        buffer = self.stack[0]
        self.stack.pop(0)
        self.stack.append(buffer)
    #clears given register (15)
    def clear_reg(self, register):
        if register in ('a','b','c','d', 'e', 'f', 'g', 'h'):
            self.registers[register] = [None, None]
        else:
            print("RunTime Error: on line %d, register %s does not exist" % (register, self.linepointer+1))
    #Main RunTime
    def RunTime(self, code_list):
        print("RunTime: Starting")
        self.linepointer = 0
        self.runtime = True
        self.startfound = False
        #pre runs labels to find start of file
        for line in code_list:
            #this checks if the line is a section
            if line[0] == 9:
                if line[1] == "Start":
                    self.sec(line[1], code_list.index(line))
                    self.linepointer = code_list.index(line) + 1
                    self.startfound = True
                    continue
                self.sec(line[1], code_list.index(line))
        #Make sure start was found
        if not self.startfound:
            print("PreRunTimeChecker Error: _Start: label not found, _Start: label is nessicary")
            sys.exit()
        #chooses what command to run when starting each line
        while self.runtime:
            try:
                tline = code_list[self.linepointer]
            except IndexError:
                print("RunTime Error: Line pointer went out of range, needs to finish at a 'end' statment")
                sys.exit()
            lncmd = int(tline[0])
            if lncmd in (1, 5, 6, 7, 8):
                self.instructions[lncmd](tline[1], tline[2])
                self.linepointer += 1
                continue
            if lncmd in (2, 3, 4, 10, 13, 15):
                self.instructions[lncmd](tline[1])
                self.linepointer += 1
                continue
            if lncmd == 9:
                self.linepointer += 1
                continue
            if lncmd in (11, 12):
                self.instructions[lncmd](tline[1], tline[2], tline[3])
                self.linepointer += 1
                continue
            if lncmd == 14:
                self.instructions[lncmd]()
                self.linepointer += 1
                continue
            if lncmd == 255:
                print("RunTime: Finished")
                self.runtime = False
    def delete(self):
        print("VM: Disassembing")
        del self.section
        del self.stack
        del self.dict
        del self.registers
        del self.instructions

def Main():
    print("Main: Starting")
    try:
        compiled_code = compiler(sys.argv[1])
    except:
        compiled_code = compiler("code.foxasm")
    fox = vm()
    fox.RunTime(compiled_code)
    fox.delete()
    del fox
    del compiled_code
    print("Main: Finished")

if __name__ == "__main__":
    Main()
    