# This is a solution to the Advent Of Code 2018 puzzle - Day 19 "Go With The Flow".
# https://adventofcode.com/2018/day/19
#
# Code based on solution to Day 16 "Chronal Classification".

# These next 16 functions, are the functionality of the device's 16 opcodes.

def addr (regs, a, b):
    return regs[a] + regs[b]

def addi (regs, a, b):
    return regs[a] + b

def mulr (regs, a, b):
    return  regs[a] * regs[b]

def muli (regs, a, b):
    return regs[a] * b

def banr (regs, a, b):
    return regs[a] & regs[b]

def bani (regs, a, b):
    return regs[a] & b

def borr (regs, a, b):
    return regs[a] | regs[b]

def bori (regs, a, b):
    return regs[a] | b

def setr (regs, a, b):
    return regs[a]

def seti (regs, a, b):
    return a

def gtir (regs, a, b):
    if a > regs[b]:
        return 1
    else:
        return 0

def gtri (regs, a, b):
    if regs[a] > b:
        return 1
    else:
        return 0

def gtrr (regs, a, b):
    if regs[a] > regs[b]:
        return 1
    else:
        return 0

def eqir (regs, a, b):
    if a == regs[b]:
        return 1
    else:
        return 0

def eqri (regs, a, b):
    if regs[a] == b:
        return 1
    else:
        return 0

def eqrr (regs, a, b):
    if regs[a] == regs[b]:
        return 1
    else:
        return 0


class Device:

    def __init__(self):
        self.registers = [0, 0, 0, 0, 0, 0]         # List of 6 registers (numbered 0 thru 5]

        # Dictionary of instructions that a device can execute. Key=Name(string), Value=Function.
        self.instructions = {"addr": addr, "addi": addi, "mulr": mulr, "muli": muli,
                             "banr": banr, "bani": bani, "borr": borr, "bori": bori,
                             "setr": setr, "seti": seti, "gtir": gtir, "gtri": gtri,
                             "gtrr": gtrr, "eqir": eqir, "eqri": eqri, "eqrr": eqrr}

        self.instruction_pointer = 0                # Which line of code will be executed next.
        self.ip_binding = 0                         # Which register number is the Instruction Pointer bound to.
        self.program = {}                           # Key=Code line, Value=(Operation, List of parms).
        self.last_line_of_code = 0                  # Line number of the last line of code in the program.
        self.debug = False                          # When True, print debug info as each line of code is executed.


    def execute_program_line(self):                 # Run the line of code in the program pointed to by the IP.

        # Get the instruction and parms for the line of code that the IP is currently pointing at.
        (instruction, parms) = self.program.get(self.instruction_pointer)

        # Update the bound register to the current value of the IP.
        self.registers[self.ip_binding] = self.instruction_pointer

        # Print status of device before instruction is executed.
        if self.debug:
            print("ip=%d" % self.instruction_pointer, self.registers, instruction, parms, "", end="")

        # Execute the instruction.
        a = parms[0]                                # Split out the parm list into named variables: a, b, and c.
        b = parms[1]
        c = parms[2]                                # ...
        self.registers[c] = instruction(self.registers, a, b)

        # Set the IP to the value of the bound register.
        self.instruction_pointer = self.registers[self.ip_binding]

        # Add 1 to the IP.
        self.instruction_pointer += 1

        if self.debug:
            print(self.registers)                   # Print the status of registers after instruction executed.


    def execute_program(self):
        # Execute program lines until the IP goes past last line of code.
        while (self.instruction_pointer <= self.last_line_of_code):
            self.execute_program_line()


    def load_program(self, filename):
        line_no = -1
        with open(filename) as fileobj:
            for line in fileobj:
                if line_no == -1:
                    clean = (line.lstrip("#ip ")).rstrip("]\n")
                    self.ip_binding = int(clean)
                else:
                    instruction = line[0:4]
                    instruction_func = self.instructions.get(instruction)

                    parms = list(map(int, ((line[5:].rstrip("]\n"))).split(" ")))

                    self.program[line_no] = (instruction_func, parms)

                line_no += 1

        self.last_line_of_code = line_no -1


# Test data.
test_device = Device()
test_device.debug = True
test_device.load_program("test1.txt")
test_device.execute_program()
print("Test Data... Register 0:", test_device.registers[0])

# Part 1.
part1_device = Device()
part1_device.load_program("input.txt")
part1_device.execute_program()
print("Part 1... Register 0:", part1_device.registers[0])
