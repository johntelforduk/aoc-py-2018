# This is a solution to the Advent Of Code 2018 puzzle - Day 13
# https://adventofcode.com/2018/day/13
from typing import List, Any

class Cart:
    def __init__(self, start_x, start_y, start_symbol):     # A Cart has...
        self.coords = (start_x, start_y)                    # current coordinates on the track.
        self.symbol = start_symbol                          # a current symbol (^ > < v),
        self.next_intersection = "L"                        # a next choice at intersection (L S R).
        self.last_tick = 0                                  # what tick number did it last move on?

    def __str__(self):                                      # Return the coordinates of cart in form "(1, 2)".
        x, y = self.coords
        tup_str = "(" + str(x) + ", " + str(y) + ")"
        return tup_str

    def rotate_left(self):                                  # "Left" = counter-clockwise.
        self.symbol = {"^" : "<", ">" : "^", "v" : ">", "<" : "v"}.get(self.symbol)

    def rotate_right(self):                                 # "Right" = clockwise.
        self.symbol = {"^" : ">", ">" : "v", "v" : "<", "<" : "^"}.get(self.symbol)

    def intersection(self):                                 # When cart has reached an intersection "+".
        if self.next_intersection == "L":
            self.rotate_left()
            self.next_intersection = "S"
        elif self.next_intersection == "S":
            self.next_intersection = "R"
        else:
            self.rotate_right()
            self.next_intersection = "L"

    def forward(self, curr_tick):
        curr_x, curr_y = self.coords                        # Unpack the coordinates tuple.
        self.coords = \
            (curr_x + {">" : 1, "<" : -1}.get(self.symbol, 0), \
             curr_y + {"v" : 1, "^" : -1}.get(self.symbol, 0))

        self.last_tick = curr_tick

class Railway:
    def __init__(self):                     # A railways has...
        self.layout = {}                    # track layout,
        self.carts = []                     # list of carts,
        self.width = 0                      # known width of the layout,
        self.height = 0                     # known height of the layout,
        self.crash = False                  # have there been any crashes yet?
        self.crash_coords = (0, 0)          # coordinates of the first crash,
        self.ticks = 0                      # a counter of how many ticks have been played so far.

    def load(self, filename):
        x = 0
        y = 0
        with open(filename) as fileobj:
            for line in fileobj:
                if x > self.width:
                    self.width = x
                x = 0
                for ch in line:

                    if ch in "^><v":                    # Is the char a cart symbol?
                        # Figure out which bit of track was behind the cart.
                        self.layout[(x,y)] = {"^" : "|", ">" : "-", "v" : "|", "<" : "-"}.get(ch)

                        new_cart = Cart(x, y, ch)       # Create a new cart.
                        self.carts.append(new_cart)     # Add the new cart to the list of carts.

                        x += 1

                    elif ch != "\n":                    # Don't store newline chars in the railway layout.
                        self.layout[(x, y)] = ch
                        x += 1
                y += 1
        self.height = y

    def print(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.crash and (x, y) == self.crash_coords:          # Was there a crash at this position?
                    print("X", end="")
                else:
                    found_a_cart=False
                    for c in self.carts:                                # Is there a cart at this position?
                        if (x, y) == c.coords:
                            print(c.symbol, end="")
                            found_a_cart=True
                    if not(found_a_cart):                               # No crash, no cart, so print the map.
                        print(self.layout.get((x, y), ""), end="")
            print()                                                     # End of a row, so start a new line.

    def remove_cart(self, dead_cart):                                   # Remove a crashed cart from railway system.
        self.carts.remove(dead_cart)

    def crash_test(self):                                               # 2 carts on same square of the layout?
        for a in self.carts:
            for b in self.carts:
                if a != b and a.coords == b.coords:                     # Carts a and b have crashed into each other.

                    if not self.crash:                                  # First crash?
                        self.crash = True
                        self.crash_coords = a.coords                    # Make note of crash coordinates.

                    self.remove_cart(a)                                 # Remove the crashed carts from the game.
                    self.remove_cart(b)

    def tick(self):                                                     # Move all of the carts by one 'tick'.
        self.ticks = self.ticks + 1                                     # Time is moving forward by 1 tick.
        for iy in range(0, self.height):
            for ix in range(0, self.width):
                for c in self.carts:
                    if (ix, iy) == c.coords and c.last_tick != self.ticks:     # ix == c.x and iy == c.y and c.last_tick != self.ticks:
                        c.forward(self.ticks)                           # Move the cart forward 1 step.
                        self.crash_test()

                        map_square = self.layout.get(c.coords, "")      # What square of the map the cart is on.

                        if map_square == "\\":                          # Go round top-right or bottom-left of a square.
                            if c.symbol in "^v":
                                c.rotate_left()
                            else:
                                c.rotate_right()

                        if map_square == "/":                           # Go round top-left or bottom-right of a square.
                            if c.symbol in "^v":
                                c.rotate_right()
                            else:
                                c.rotate_left()

                        if map_square == "+":                           # Turn (or go straight on) at an intersection.
                            c.intersection()

# This solves Part 1 of the puzzle.
track=Railway()
track.load("test2.txt")

track.print()

while track.crash is False:
    track.tick()

track.print()

print ("First crash at ", end=""); print (track.crash_coords)


# This solves Part 2 of the puzzle.
track2=Railway()
track2.load("test3.txt")

track2.print()

carts_left = 999

while carts_left > 1:
    track2.tick()
    num_carts = len(track2.carts)
    if num_carts != carts_left:
        print ("Carts left %d" % (num_carts))
        carts_left = num_carts
track2.print()

print ("Last cart at ", end="")
for c in track2.carts:
    print (c)