# This is a solution to the Advent Of Code 2018 puzzle - Day 18 "Settlers of The North Pole".
# https://adventofcode.com/2018/day/18

class Forest:

    def __init__(self):
        self.area = {}              # The lumber collection area. Key=(x, y) co-ords, Value=contents of that acre.
        self.max_x = 0              # Max coordinates of the area...
        self.max_y = 0              # ...
        self.minutes = 0            # How many minutes old is the forest.

    def load(self, filename):
        y = 0
        with open(filename) as fileobj:
            for line in fileobj:
                for x in range(0, len(line)):
                    if line[x] != "\n":                 # Because we don't need the \n at end of line in the dictionary.
                        self.area[(x, y)] = line[x]
                        if x > self.max_x:
                            self.max_x = x
                y += 1                                  # Increment y at end of each line.
        self.max_y = y - 1

    def print(self):
        print("Minutes:", self.minutes)
        for y in range(0, self.max_y + 1):
            for x in range(0, self.max_x + 1):
                print(self.area.get((x, y)), end="")
            print()

    def one_minute(self):
        target = Forest()

        for y in range(0, self.max_y + 1):              # Look at each square in turn.
            for x in range(0, self.max_x + 1):

                # Make a list of neighbors.
                neighbours = []
                for dx in range(-1, 2):                 # Delta x.
                    for dy in range(-1, 2):             # Delta y.
                        if dx != 0 or dy !=0:           # This square is not its own neighbour.
                            this_x = x + dx
                            this_y = y + dy

                            this_acre = self.area.get((this_x, this_y), "")
                            if this_acre != "":
                                neighbours.append(this_acre)

                num_trees = 0
                num_lumberyards = 0
                for n in neighbours:
                    if n == "|":
                        num_trees += 1
                    if n == "#":
                        num_lumberyards += 1

                this_acre = self.area.get((x, y))

                # "An open acre will become filled with trees if three or more adjacent acres contained trees.
                # Otherwise, nothing happens."
                if this_acre == ".":
                    if num_trees >= 3:
                        target.area[(x, y)] = "|"
                    else:
                        target.area[(x, y)] = this_acre

                # "An acre filled with trees will become a lumberyard if three or more adjacent acres were lumberyards.
                # Otherwise, nothing happens."
                if this_acre == "|":
                    if num_lumberyards >= 3:
                        target.area[(x, y)] = "#"
                    else:
                        target.area[(x, y)] = this_acre

                # "An acre containing a lumberyard will remain a lumberyard if it was adjacent to at least one other
                # lumberyard and at least one acre containing trees. Otherwise, it becomes open."
                if this_acre == "#":
                    if num_lumberyards >= 1 and num_trees >= 1:
                        target.area[(x, y)] = this_acre
                    else:
                        target.area[(x, y)] = "."

        self.area = target.area                         # Copy target area to main object's area.
        self.minutes += 1


def total_resource(a_forest):                           # total_resource = count(trees) * count(lumberyards)
    num_trees = 0
    num_lumberyards = 0

    for y in range(0, a_forest.max_y + 1):              # Look at each square in turn.
        for x in range(0, a_forest.max_x + 1):

            if a_forest.area.get((x, y)) == "|":
                num_trees += 1

            if a_forest.area.get((x, y)) == "#":
                num_lumberyards += 1

    return (num_trees * num_lumberyards)


def frequencies(lst):
    d = {}
    for i in lst:
        if d.get(i):
            d[i] += 1
        else:
            d[i] = 1
    return d


# Solution to Part 1.
my_forest = Forest()
my_forest.load("input.txt")

my_forest.print()

for i in range(0, 10):
    my_forest.one_minute()
    print()
    my_forest.print()

print("Total resource:", total_resource(my_forest))


# Solution to Part 2.
# This code demonstrates that - after a while - the patterns repeat every 28 minutes.
#
# 1000000000 - (28 * 35714251) = 972
# Therefore, whatever the Total Resource value was on minute 972, it will be the same on minute 1000000000.

# my_old_forest = Forest()
# my_old_forest.load("input.txt")
#
# my_old_forest.print()
#
# forest_list = []
#
# forest_list.append(total_resource(my_old_forest))
#
# for i in range(0, 972):
#     my_old_forest.one_minute()
#
#     this_resource = total_resource(my_old_forest)
#     forest_list.append(total_resource(my_old_forest))
#
#     if this_resource == 197050:
#         print()
#         my_old_forest.print()
#
# print (forest_list)
# freq = frequencies(forest_list)
#
# for k, v in freq.items():
#     print (k, v)
#
# print(total_resource(my_old_forest))
