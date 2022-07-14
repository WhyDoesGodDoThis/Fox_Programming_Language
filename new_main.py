import sys
class VM:
    def __init__(self):
        print("VM: Assembling")
        self.null = None
        self.instructions = {
            1: self.move,
            2: self.load,
            3: self.unload,
            4: self.set_reg,
            5: self.clear_reg,
            6: self.jmp,
            7: self.jel,
            8: self.jnl,
            9: self.jls,
            10: self.jgr,
            11: self.jll,
            12: self.jgl,
            13: self.section,
            14: self.add,
            15: self.sub,
            16: self.mul,
            17: self.div,
            18: self.pnt,
            19: self.sar,
            20: self.ssr,
            21: self.smr,
            22: self.sdr,
            23: self.null,
            24: self.null,
            25: self.null,
            26: self.null,
            27: self.null,
            254: self.end
        }
        self.registers = {
            'a': [None, None], #default for add
            'b': [None, None], #default for sub
            'c': [None, None], #default for mul
            'd': [None, None], #default for div
            'e': [None, None], 
            'f': [None, None], 
            'g': [None, None],
            'h': [None, None],
            'i': [None, None],
            'j': [None, None], #logic for jump
            'k': [None, None], #for print
            'l': [None, None],
            'm': [None, None],
            'n': [None, None]
        }
        self.add_reg = 'a'
        self.sub_reg = 'b'
        self.mul_reg = 'c'
        self.div_reg = 'd'
        self.stack = []
        self.variables = {}
        self.sections = {}
        self.linepointer = 0
        self.runtime = False
        print("VM: Assembled")

    #move value to variable (1)

    def move(self, value, variable, type_=int):
        try:
            value = variables[str(value)]
        except KeyError:
            pass
        if "reg_" in value:
            value = self.registers[value[-2]][-1]
        self.variables[variable] = type_(value)

    #load variable to stack (2)
    def load(self, variable):
        if varible in self.stack:
            self.stack.pop(self.stack.index(variable))
        self.stack.insert(0, varible)

    #unload variable from stack (3)
    def unload(self, variable):
        if varible in self.stack:
            self.stack.pop(self.stack.index(variable))

    #set register to value (4)
    def set_reg(self, register):
        self.registers[register[0]][int(register[1])] = variables[stack[0]]

    #clear register (5)
    def clear_reg(self, register):
        self.registers[register[0]] = [None, None]

    #set section (6)
    def section(self, name, line):
        self.sections[name] = line

    #jump to section (7)
    def jmp(self, section):
        self.linepointer = self.sections[section]

    #jump to section if equal (8)
    def jel(self, section):
        if self.registers['j'][0] == self.registers['j'][1]:
            self.linepointer = self.sections[section]

    #jump to section if not equal (9)
    def jnl(self, section):
        if self.registers['j'][0] != self.registers['j'][1]:
            self.linepointer = self.sections[section]

    #jump to section if less (10)
    def jls(self, section):
        if self.registers['j'][0] < self.registers['j'][1]:
            self.linepointer = self.sections[section]

    #jump to section if greater (11)
    def jgr(self, section):
        if self.registers['j'][0] > self.registers['j'][1]:
            self.linepointer = self.sections[section]

    #jump to section if less or equal (12)
    def jll(self, section):
        if self.registers['j'][0] <= self.registers['j'][1]:
            self.linepointer = self.sections[section]

    #jump to section if greater or equal (13)
    def jgl(self, section):
        if self.registers['j'][0] >= self.registers['j'][1]:
            self.linepointer = self.sections[section]

    #add (14)
    def add(self, varible):
        variables[variable] = self.registers[self.add_reg][0] + self.registers[self.add_reg][1]

    #sub (15)
    def sub(self, varible):
        variables[variable] = self.registers[self.sub_reg][0] - self.registers[self.sub_reg][1]

    #mul (16)
    def mul(self, varible):
        variables[variable] = self.registers[self.mul_reg][0] * self.registers[self.mul_reg][1]

    #div (17)
    def div(self, varible):
        variables[variable] = self.registers[self.div_reg][0] / self.registers[self.div_reg][1]

    #print (18)
    def pnt(self):
        print(registers['k'][0])

    #set add register (19)
    def sar(self, register):
        self.add_reg = register

    #set sub register (20)
    def ssr(self, register):
        self.sub_reg = register

    #set mul register (21)
    def smr(self, register):
        self.mul_reg = register

    #set div register (22)
    def sdr(self, register):
        self.div_reg = register

    #end runtime (not instruction)
    def end(self):
        print("RunTime: Finished")
        self.runtime = False
    
    #delete main parts of VM (not instruction)
    def delete(self):
        print("VM: Disassembling")
        del self.null
        del self.add_reg
        del self.sub_reg
        del self.mul_reg
        del self.div_reg
        del self.registers
        del self.stack
        del self.variables
        del self.sections
        del self.runtime
        del self.linepointer
        del self.instructions
        print("VM: Disassembled")
    
    #RunTime where main code is ran
    def RunTime(self, code):
        #pre runtime checks and runs labels
        start = False
        for index, line in enumerate(code, start=1):
            line = bytearray(line)
            if line[0] == 6:
                if line[1:] == b'Start':
                    start = True
                self.section(line[1:].decode(), index)
        #runtime
        if start:
            self.runtime = True
        else:
            print(self.sections)
            sys.exit()
        print("RunTime: Starting")
        while self.runtime:
            tline = code[self.linepointer]
            lncmd = int(tline[0])
            if lncmd in (254, 18):
                self.instructions[tline[0]]()
                self.linepointer+=1
                continue
            if lncmd in (2,3,4,5,6,7,8,9,10,11,12,14,15,16,17,19,20,21,22):
                self.instructions[tline[0]](tline[1:].decode())
                self.linepointer+=1
                continue
            if lncmd == 1:
                mov_args = tline[1:].split(b'\xee')
                self.instructions[tline[0]](mov_args[1].decode(),mov_args[2].decode(),mov_args[3].decode())
                self.linepointer+=1
                continue
            self.linepointer+=1
def preCompile(bytecode):
    code = bytearray(bytecode)
    code = code.split(b'\xff\xff')
    return code
    
def Main():
    vm = VM()
    vm.RunTime(preCompile(open("main.foxbin", "rb").read()))
    vm.delete()
    del vm

if __name__ == "__main__":
    Main()