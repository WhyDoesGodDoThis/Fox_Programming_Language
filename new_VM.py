class VM:
    def __init__(self):
        print("VM: Assembling")
        self.null = None
        self.instructions = {
            b'\0x01': self.move,
            b'\0x02': self.load,
            b'\0x03': self.unload,
            b'\0x04': self.set_reg,
            b'\0x05': self.clear_reg,
            b'\0x06': self.jmp,
            b'\0x07': self.jel,
            b'\0x08': self.jnl,
            b'\0x09': self.jls,
            b'\0x0a': self.jgr,
            b'\0x0b': self.jll,
            b'\0x0c': self.jgl,
            b'\0x0d': self.section,
            b'\0x0e': self.add,
            b'\0x0f': self.sub,
            b'\0x10': self.mul,
            b'\0x11': self.div,
            b'\0x12': self.pnt,
            b'\0x13': self.sar,
            b'\0x14': self.ssr,
            b'\0x15': self.smr,
            b'\0x16': self.sdr,
            b'\0x17': self.null,
            b'\0x18': self.null,
            b'\0x19': self.null,
            b'\0x1a': self.null,
            b'\0x1b': self.null,
            b'\0xff': self.end
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
            if line[0] == b'\0x0d':
                if line[1:] == b'S':
                    start = True
                self.section(line[1:], index)
        #runtime
        print("RunTime: Starting")
        self.runtime = True
        while self.runtime:
            tline = code[self.linepointer]
            lncmd = int(tline[0], 16)
            if lncmd in (255, 18):
                self.instructions[tline[0]]()
                self.linepointer+=1
                continue
            if lncmd in (2,3,4,5,6,7,8,9,10,11,12,14,15,16,17,19,20,21,22):
                self.instructions[tline[0]](tline[1:].decode())
                self.linepointer+=1
                continue
            self.linepointer+=1