"""CPU functionality."""

import sys

# Adding Binary 
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
                # memory bytes
        self.ram = [0] * 256
        # 8 general purpose geisters
        self.reg = [0] * 8
        # internal register counter
        self.pc = 0
        # later will set the initial value of the stack pointer


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

          print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.pc,
                # self.fl,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ),
            end="",
        )
        for i in range(8):
            print(" %02X" % self.reg[i], end="")

        print()
  def ram_read(self, MAR):
        # accept the address to read and return the value stored
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        # accept a value to write, an address to write to
        # MAR is the memory address register, MDR is the memory data register
        # write the value -> MDR to the address MAR
        self.ram[MAR] = MDR

    def hlt(self):
        # stop the program by calling it in the run function
        self.running = False

    def ldi(self):
        #### LDI
        # `LDI register immediate`
        # Set the value of a register to an integer.
        # Machine code:
        # ```
        # 10000010 00000rrr iiiiiiii
        # 82 0r ii
        # ```
        # 0b10000010,  # LDI R0,8 128->dec

        # sets a specific register to a specified value
        operand_a = self.ram[self.pc + 1]
        operand_b = self.ram[self.pc + 2]
        self.reg[operand_a] = operand_b
        self.pc += 3

    def prn(self):
        operand_a = self.reg[self.pc + 1]
        print(self.reg[operand_a])
        self.pc += 2

    def run(self):
        """Run the CPU."""
              self.running = True
        while self.running:
            # needs to read the emmeory address thats stored in the regester PC
            # store the result in the IR

            ir = self.pc
            inst = self.ram[ir]
            # if else chain to deal with the program
            if inst == LDI:
                self.ldi()
            elif inst == HLT:
                self.hlt()
            elif inst == PRN:
                self.prn()



# 
# 
# 
#  """CPU functionality."""

# import sys

# class CPU:
#     """Main CPU class."""

#     def __init__(self):
#         """Construct a new CPU."""
#         pass

#     def load(self):
#         """Load a program into memory."""

#         address = 0

#         # For now, we've just hardcoded a program:

#         program = [
#             # From print8.ls8
#             0b10000010, # LDI R0,8
#             0b00000000,
#             0b00001000,
#             0b01000111, # PRN R0
#             0b00000000,
#             0b00000001, # HLT
#         ]

#         for instruction in program:
#             self.ram[address] = instruction
#             address += 1


#     def alu(self, op, reg_a, reg_b):
#         """ALU operations."""

#         if op == "ADD":
#             self.reg[reg_a] += self.reg[reg_b]
#         #elif op == "SUB": etc
#         else:
#             raise Exception("Unsupported ALU operation")

#     def trace(self):
#         """
#         Handy function to print out the CPU state. You might want to call this
#         from run() if you need help debugging.
#         """

#         print(f"TRACE: %02X | %02X %02X %02X |" % (
#             self.pc,
#             #self.fl,
#             #self.ie,
#             self.ram_read(self.pc),
#             self.ram_read(self.pc + 1),
#             self.ram_read(self.pc + 2)
#         ), end='')

#         for i in range(8):
#             print(" %02X" % self.reg[i], end='')

#         print()

#     def run(self):
#         """Run the CPU."""
#         pass
