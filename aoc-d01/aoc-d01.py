# This is a solution to parts 1 and 2 of the Advent Of Code 2018 puzzle - Day 1
# https://adventofcode.com/2018/day/1

import re

f = open("input.txt")
whole_text = (f.read())
string_list = re.split('\n', whole_text)    # Split into words by white-space, commas or full-stops.
number_list=[int(x) for x in string_list]   # Convert list of strings to list of integers.

# Part One of the puzzle.
sumation=0

for x in number_list:
    sumation += x

print("Part 1 : %d" % (sumation))

# Part Two of the puzzle.
sumation=0
previously_seen=[]
found=False

print("Working.", end="")       # Part Two takes a few mins to run, so we'll print "Working......"

while not(found):
    print(".", end="")
    for x in number_list:
        sumation += x
        if previously_seen.count(sumation) > 0:
            found=True
            break
        previously_seen.append(sumation)

print("\nPart 2 : %d" % (sumation))