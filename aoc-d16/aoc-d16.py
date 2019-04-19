# This is a solution to the Advent Of Code 2018 puzzle - Day 16 "Chronal Classification".
# https://adventofcode.com/2018/day/16

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
        self.registers = [0, 0, 0, 0]               # List of 4 registers (numbered 0 thru 3]

        # List of instructions that a device can execute.
        self.instructions = [addr, addi, mulr, muli, banr, bani, borr, bori,
                             setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

        self.opcodes = {}                           # Key=opcode, Value=instruction.

        self.test_data = []                         # Test data in memory, loaded from file.
        self.three_or_more = 0                      # Count of tests which behave like 3 or more opcodes.


    # Call the parm function, passing it parm integers a and b, and store the result in register [c].
    def execute_instruction(self, instruction, a, b, c):
        self.registers[c] = instruction(self.registers, a, b)


    def obtain_test_data(self, filename):
        quad = 0
        with open(filename) as fileobj:
            for line in fileobj:
                if quad == 0:
                    clean = (line.lstrip("Before: [")).rstrip("]\n")
                    before = list(map(int, clean.split(", ")))

                if quad == 1:
                    instruction = list(map(int, line.split(" ")))

                if quad == 2:
                    clean = (line.lstrip("After: [")).rstrip("]\n")
                    after = list(map(int, clean.split(", ")))

                if quad == 3:
                    tuple = (before, instruction, after)
                    self.test_data.append(tuple)

                quad = (quad + 1) % 4


    def count_triples(self):
        self.three_or_more = 0

        for t in self.test_data:
            (test_before, test_instruction, test_after) = t
            matches = 0

            for i in self.instructions:
                self.registers = test_before.copy()
                self.execute_instruction(i, test_instruction[1], test_instruction[2], test_instruction[3])
                if self.registers == test_after:
                    matches += 1

            if matches >= 3:
                self.three_or_more += 1


    def discover_opcodes(self):
        unclaimed_opcodes = list(range(0, 16))

        while len(unclaimed_opcodes) > 0:

            opcode_matches = []

            for i in self.instructions:

                for poss_opcode in unclaimed_opcodes:               # Loop through possible opcodes.
                    misses = 0

                    for t in self.test_data:
                        (test_before, test_instruction, test_after) = t

                        if poss_opcode == test_instruction[0]:      # This test is for the possible opcode.
                            self.registers = test_before.copy()
                            self.execute_instruction(i, test_instruction[1], test_instruction[2], test_instruction[3])

                            if self.registers != test_after:
                                misses += 1

                    if misses == 0:                                 # No misses, so possible opcode might be the opcode.
                            opcode_matches.append((i, poss_opcode))

            # Go through list of opcode matches, and make a dictionary of opcode match frequencies.
            dist = {}
            for om in opcode_matches:
                (f, o) = om
                if dist.get(f):
                    dist[f] += 1
                else:
                    dist[f] = 1

            # Any instruction with a single match must be an Opcode=Instruction match.
            for k in dist.keys():
                matches = dist[k]

                if matches == 1:
                    # Add to dictionary of opcodes, Remove from list of unclaimed opcodes.

                    for match in opcode_matches:
                        (instruction, opcode) = match

                        if k == instruction:
                            self.opcodes[opcode] = instruction      # Add opcode: instruction to dictionary.
                            unclaimed_opcodes.remove(opcode)        # Remove the opcode from list of unclalimed opcodes.


    def run_program(self, filename):
        self.registers = [0, 0, 0, 0]                               # Initialise all of the registers to zero.

        with open(filename) as fileobj:
            for line in fileobj:
                instruction = list(map(int, line.split(" ")))       # Parse each program line into list of 4 integers.
                i = self.opcodes.get(instruction[0])                # Lookup the function for this opcode.
                self.execute_instruction(i, instruction[1], instruction[2], instruction[3])


test_device = Device()
test_device.obtain_test_data("test2.txt")

# Part 1 of the puzzle.
test_device.count_triples()
print("Tests with 3 or more matches:", test_device.three_or_more)

# Part 2 of the puzzle.
test_device.discover_opcodes()
test_device.run_program("test_program.txt")
print("Register 0:", test_device.registers[0])