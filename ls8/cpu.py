import sys


HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
PUSH = 0b01000101
POP = 0b01000110

# PC
CALL = 0b01010000
RET = 0b00010001
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

# ALU
MUL = 0b10100010
ADD = 0b10100000
CMP = 0b10100111


# Main CPU class
class CPU:
    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7  # stack pointer is always register 7
        self.fl = 0
        self.dispatchtable = {
            MUL: self.mul,
            ADD: self.add,
            CMP: self.cmp,
            PRN: self.prn,
            LDI: self.ldi,
            PUSH: self.push,
            POP: self.pop,
            CALL: self.call,
            RET: self.ret,
            JMP: self.jmp,
            JEQ: self.jeq,
            JNE: self.jne
        }


    # Load a program into memory
    def load(self, file_name):
        address = 0
        with open(file_name, 'r') as f:
            for line in f:
                if line.startswith('#') or line.startswith('\n'):
                    continue
                else:
                    instruction = line.split(' ')[0]
                    self.ram[address] = int(instruction, 2)
                    address += 1

    # Read RAM at given address, return value
    def ram_read(self, mar):
        return self.ram[mar]

    # Write value at given address
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    # ALU operations
    def alu(self, op, reg_a, reg_b):
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            self.fl = 1 if self.reg[reg_a] == self.reg[reg_b] else 0
        else:
            raise Exception("Unsupported ALU operation")

    # Handy function to print out the CPU state. 
    # You might want to call this from run() if you need help debugging.
    def trace(self):
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')
        for i in range(8):
            print(" %02X" % self.reg[i], end='')
        print()
    def mul(self, reg_a, reg_b):
        self.alu("MUL", reg_a, reg_b)
        self.pc += 3
    def add(self, reg_a, reg_b):
        self.alu("ADD", reg_a, reg_b)
        self.pc += 3
    def cmp(self, reg_a, reg_b):      # Handle CMP with Equal flag
        self.alu("CMP", reg_a, reg_b)
        self.pc += 3
    def prn(self, reg_a, reg_b):
        print(self.reg[reg_a])
        self.pc += 2
    def ldi(self, reg_a, reg_b):
        self.reg[reg_a] = reg_b
        self.pc += 3
    def push(self, reg_a, reg_b):
        self.sp -= 1
        self.ram_write(self.sp, self.reg[reg_a])
        self.pc += 2
    def pop(self, reg_a, reg_b):
        self.reg[reg_a] = self.ram_read(self.sp)
        self.sp += 1
        self.pc += 2
    def call(self, reg_a, reg_b):
        self.sp -= 1
        self.ram_write(self.sp, self.pc + 2)
        self.pc = self.reg[reg_a]
    def ret(self, reg_a, reg_b):
        self.pc = self.ram_read(self.sp)
        self.sp += 1
    def jmp(self, reg_a, reg_b):
        self.pc = self.reg[reg_a]
    def jeq(self, reg_a, reg_b):
        if self.fl:
            self.jmp(reg_a, reg_b)
        else:
            self.pc += 2       
    def jne(self, reg_a, reg_b):
        if not self.fl:
            self.jmp(reg_a, reg_b)
        else:
            self.pc += 2
    def run(self):
        running = True
        # Run the CPU
        while running:
            ir = self.ram_read(self.pc)
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)

            if ir == HLT:
                running = False
            else:
                self.dispatchtable[ir](reg_a, reg_b)







# """CPU functionality."""

# import sys

# class CPU:
#     """Main CPU class."""

#     def __init__(self):
#         """Construct a new CPU."""
#         self.ram = [0] * 256
#         self.pc = 0
#         self.reg = [0] * 8
#         self.HLT = 0b00000001
#         self.MUL = 0b10100010
#         self.PUSH = 0b01000101
#         self.POP = 0b01000110
#         self.address = 0
#         self.ADD = 0b10100000
#         self.CALL = 0b01010000
#         self.RET = 0b00010001
#         self.sp = 7  # stack pointer is always register 7
#         # sprint
#         self.JMP = 0b01010100
#         self.JEQ = 0b01010101
#         self.JNE = 0b01010110
#         self.CMP = 0b10100111
#         self.fl = 0

#     def load(self, file=None):
#         """Load a program into memory."""
#         if file==None:
#             file=sys.argv[1]
#         with open(file) as f:
#             for line in f:
#                 try:
#                     line = line.strip().split("#",1)[0]
#                     line = int(line, 2)
#                     self.ram[self.address] = line
#                     self.address += 1
#                 except ValueError:
#                     pass

#     def alu(self, op, operand_a, operand_b):
#         """ALU operations."""

#         if op == "ADD":
#             self.reg[operand_a] += self.reg[operand_b]
#             self.pc += 3
#         elif op == self.MUL:
#             self.reg[operand_a] *= self.reg[operand_b]
#         elif op == "CMP":
#             self.fl = 1 if self.reg[operand_a] == self.reg[operand_b] else 0
#         else:
#             raise Exception("Unsupported ALU operation")

#     def ram_read(self, mar):
#         return self.ram[mar]

#     # Needed to switch address and value to the correct places 
#     def ram_write(self, address=None, value=None):
#         self.ram[address] = value
   
#     #  This is the same as above 
#     # def ram_write(self, mar, mdr):
#     #     self.ram[mar] = mdr  

#     def trace(self):
#         """
#         Handy function to print out the CPU state. You might want to call this
#         from run() if you need help debugging.
#         """

#         print(f"TRACE: %02X | %02X %02X %02X |" % (
#             self.pc,
#             self.ram_read(self.pc),
#             self.ram_read(self.pc + 1),
#             self.ram_read(self.pc + 2)
#         ), end='')

#         for i in range(8):
#             print(" %02X" % self.reg[i], end='')

#         print()    

#     def run(self):
#         """Run the CPU."""
#         self.trace()
#         running = True
#         while running:
#             IR = self.ram_read(self.pc)
#             operand_a = self.ram_read(self.pc + 1)
#             operand_b = self.ram_read(self.pc + 2)
#             if IR ==  0b10000010:  # LDI instruction
#                 self.reg[operand_a] = operand_b
#                 self.pc += 3
#             elif IR == 0b01000111:  # PRN instruction
#                 print(self.reg[operand_a])
#                 self.pc += 2
#             elif IR == self.ADD:
#                 op = "ADD"
#                 self.alu(op, operand_a, operand_b)
#             elif IR == self.HLT:   # Halt
#                 running = False
#             elif IR == self.MUL:
#                 # self.reg[operand_a] *= self.reg[operand_b]
#                 self.alu(IR, operand_a, operand_b)
#                 self.pc += 3
#             elif IR == self.PUSH:
#                 self.push(operand_a, operand_b)
#             elif IR == self.POP:
#                 self.pop(operand_a, operand_b)
#             elif IR == self.CALL:
#                 self.call(operand_a, operand_b)
#             elif IR == self.RET:
#                 self.ret(operand_a, operand_b)
#             elif IR == self.JMP: # Jump
#                 self.jmp(operand_a, operand_b)
#             elif IR == self.JEQ: # Jump if equal
#                 self.jeq(operand_a, operand_b)
#             elif IR == self.JNE: # Jump if not equal
#                 self.jne(operand_a, operand_b)
#             elif IR == self.CMP:
#                 op = "CMP" 
#                 self.alu(op, operand_a, operand_b)
#             else:
#                 print(f"Unknown instruction {IR}")
#                 running = False  
#     def push(self, operand_a, operand_b):
#         # print('push')
#         # self.trace()
#         self.sp -= 1
#         self.ram_write(self.sp, self.reg[operand_a])
#         self.pc += 2
#         self.trace()
#     def pop(self, operand_a, operand_b):
#         # print('pop')
#         # self.trace()
#         self.reg[operand_a] = self.ram_read(self.sp)
#         self.sp += 1
#         self.pc += 2
#         # self.trace()
#     def call(self, operand_a, operand_b):
#         self.sp -= 1
#         self.ram_write(self.sp, self.pc + 2)
#         self.pc = self.reg[operand_a]
#     # Sprint
#     def ret(self, operand_a, operand_b):
#         self.pc = self.ram_read(self.sp)
#         self.sp += 1
#     def jmp(self, operand_a, operand_b):
#         self.pc = self.reg[operand_a]
#     def jeq(self, operand_a, operand_b):
#         if self.fl:
#             self.jmp(operand_a, operand_b)
#         else:
#             self.pc += 2         
#     def jne(self, operand_a, operand_b):
#         if not self.fl:
#             self.jmp(operand_a, operand_b)
#         else:
#             self.pc += 2