"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 255
        self.reg = [0] * 8

    def load(self, file_load):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        try:
            with open(f"examples/{file_load}") as f:
                for line in f:
                    num = line.split("#" or "\n")[0].replace('\n', '')
                    self.ram[address] = int(num, 2)
                    address += 1
        except FileNotFoundError:
            print("file not found")

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MULTIPLY":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, reg_index):
        return self.reg[reg_index]

    def ram_write(self, value, reg_index):
        self.reg[reg_index] = value

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010

        run = True
        command = self.ram[self.pc]
        while run:
            if command == LDI:
                # load value into register
                reg_index = self.ram[self.pc + 1]
                num = self.ram[self.pc + 2]
                self.reg[reg_index] = num
                self.pc += 3
            elif command == MUL:
                reg_index1 = self.ram[self.pc + 1]
                reg_index2 = self.ram[self.pc + 2]
                self.alu("MULTIPLY", reg_index1, reg_index2)
                self.pc += 3
            elif command == PRN:
                reg_index = self.ram[self.pc + 1]
                print(self.reg[reg_index])
                self.pc += 2
            elif command == HLT:
                run = False
            else:
                print(f"invalid instruction [{self.ram[self.pc]}]")
                run = False
                self.pc += 1
            command = self.ram[self.pc]
