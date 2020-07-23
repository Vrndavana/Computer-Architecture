"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        self.HLT = 0b00000001
        self.MUL = 0b10100010
        self.PUSH = 0b01000101
        self.POP = 0b01000110
        self.address = 0
        self.sp = 7  # stack pointer is always register 7
        

    def load(self):
        """Load a program into memory."""

        with open(sys.argv[1]) as f:
            for line in f:
                try:
                    line = line.strip().split("#",1)[0]
                    line = int(line, 2)
                    self.ram[self.address] = line
                    self.address += 1
                except ValueError:
                    pass

    def alu(self, op, operand_a, operand_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[operand_a] += self.reg[operand_b]
        elif op == self.MUL:
            self.reg[operand_a] *= self.reg[operand_b]
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address=None):
        v = self.ram[address]
        return v

    # WRONG
    # def ram_write(self, value=None, address=None):
    #     self.ram[address] = value
    #  VVVVVV This one is the right VVVV
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr    
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()    

    def run(self):
        """Run the CPU."""
        self.trace()
        running = True
        while running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR ==  0b10000010:  # LDI instruction
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == 0b01000111:  # PRN instruction
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == self.HLT:   # Halt
                running = False
            elif IR == self.MUL:
                # self.reg[operand_a] *= self.reg[operand_b]
                self.alu(IR, operand_a, operand_b)
                self.pc += 3
            elif IR == self.PUSH:
                self.push(operand_a, operand_b)
            elif IR == self.POP:
                self.pop(operand_a, operand_b)
            else:
                print(f"Unknown instruction {IR}")
                running = False  
    def push(self, operand_a, operand_b):
        print('push')
        self.trace()
        self.sp -= 1
        self.ram_write(self.sp, self.reg[operand_a])
        self.pc += 2
        self.trace()
    def pop(self, operand_a, operand_b):
        # print('pop')
        # self.trace()
        self.reg[operand_a] = self.ram_read(self.sp)
        self.sp += 1
        self.pc += 2
        # self.trace()