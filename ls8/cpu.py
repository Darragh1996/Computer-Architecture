"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
ADD = 0b10100000
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 255
        self.reg = [0] * 8
        self.sp = 7
        self.reg[self.sp] = 0xf4
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[PUSH] = self.handle_push
        self.branchtable[POP] = self.handle_pop
        self.branchtable[CALL] = self.handle_call
        self.branchtable[RET] = self.handle_return
        self.branchtable[ADD] = self.handle_add

    def handle_ldi(self):
        reg_index = self.ram[self.pc + 1]
        num = self.ram[self.pc + 2]
        self.reg[reg_index] = num
        self.pc += 3

    def handle_prn(self):
        reg_index = self.ram[self.pc + 1]
        print(self.reg[reg_index])
        self.pc += 2

    def handle_mul(self):
        reg_index1 = self.ram[self.pc + 1]
        reg_index2 = self.ram[self.pc + 2]
        self.alu("MULTIPLY", reg_index1, reg_index2)
        self.pc += 3

    def handle_add(self):
        reg_index1 = self.ram[self.pc + 1]
        reg_index2 = self.ram[self.pc + 2]
        self.alu("ADD", reg_index1, reg_index2)
        self.pc += 3

    def handle_push(self):
        reg = self.ram[self.pc + 1]
        val = self.reg[reg]

        self.reg[self.sp] -= 1
        # print(self.ram[self.reg[self.sp]], self.reg[self.sp])
        # if self.ram[self.reg[self.sp]] == 0:
        self.ram[self.reg[self.sp]] = val
        self.pc += 2
        # else:
        #     self.reg[self.sp] += 1
        #     raise OverflowError("Stack Overflow")

    def handle_pop(self):
        reg = self.ram[self.pc + 1]
        val = self.ram[self.reg[self.sp]]

        self.reg[reg] = val
        self.reg[self.sp] += 1
        self.pc += 2

    def handle_call(self):
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.pc + 2

        reg = self.ram[self.pc + 1]
        self.pc = self.reg[reg]

    def handle_return(self):
        self.pc = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1

    def load(self, file_load):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        try:
            with open(f"examples/{file_load}") as f:
                for line in f:
                    num = line.split("#")[0].replace('\n', '')
                    # print(f"run -> {int(num,2):08b}")
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

        run = True
        command = self.ram[self.pc]
        while run:
            if command == HLT:
                run = False
            elif command in self.branchtable:
                self.branchtable[command]()
            else:
                print(f"invalid instruction [{self.ram[self.pc]:08b}]")
                run = False
                self.pc += 1
            command = self.ram[self.pc]

 # if command == LDI:
            #     # load value into register
            #     reg_index = self.ram[self.pc + 1]
            #     num = self.ram[self.pc + 2]
            #     self.reg[reg_index] = num
            #     self.pc += 3
            # elif command == MUL:
            #     reg_index1 = self.ram[self.pc + 1]
            #     reg_index2 = self.ram[self.pc + 2]
            #     self.alu("MULTIPLY", reg_index1, reg_index2)
            #     self.pc += 3
            # elif command == PRN:
            #     reg_index = self.ram[self.pc + 1]
            #     print(self.reg[reg_index])
            #     self.pc += 2
            # elif command == HLT:
            #     run = False
