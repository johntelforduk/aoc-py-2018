# Solution to Advent Of Code 2018, Day 9 : Marble Mania.
# https://adventofcode.com/2018/day/9


class Board:
    def __init__(self):
        self.circle = [0]                                   # The circular game board. Starts with a single 0 marble.
        self.current_marble = 0                             # Position in circle of "current marble".
        self.last_marble = 0                                # The value of the last marble played.

    def print_board(self, turn):                            # Print board in same format at AOC website example.
        print("[%d] " % turn, end="")
        x = 0
        while x < len(self.circle):
            if x == self.current_marble:
                print("(%d)" % self.circle[x], end="")      # Print brackets around the current marble.
            else:
                print(" %d " % self.circle[x], end="")      # No brackets for the other marbles.
            x += 1
        print("")                                           # After printing out the board, start a new line.

    def insert_marble(self):                                # Insert a new marble into the circle.
        if self.current_marble >= (len(self.circle) - 1):   # Special case - add marble to "end" of circle.
            self.circle.append(self.last_marble)
            self.current_marble = len(self.circle) - 1
        else:                                               # Normal case - insert the marble into circle.
            self.circle.insert(self.current_marble + 1, self.last_marble)
            self.current_marble = self.current_marble + 1

    def remove_marble(self):                                # Remove current marble from the circle.
        self.circle.remove(self.circle[self.current_marble])

    def clockwise(self):
        self.current_marble = self.current_marble + 1       # Move current marble position one place clockwise.

        if self.current_marble >= len(self.circle):         # If past end of list, rotate to start again.
            self.current_marble = 0
        return

    # Move "current marble" pointer 7 places to the left.
    def counter_clockwise_7(self):
        self.current_marble = (self.current_marble - 7) % len(self.circle)


class Game:
    def __init__(self, players, marbles):
        self.players = players                              # Number of Players in this game.
        self.marbles = marbles                              # Number of marbles in this game.
        self.board = Board()                                # Create a new board for the game.
        self.turn = 0                                       # Whose turn is it.
        self.scores = []                                    # Player scores stored in a list.
        for x in range(0, self.players):                    # Set score to zero for each player.
            self.scores.insert(0, 0)

    def next_player(self):
        self.turn += 1                                      # Turn changes to next player.
        if self.turn > self.players:
            self.turn = 1
        self.board.last_marble = self.board.last_marble + 1     # He picks up the next marble.

    def add_to_score(self, player, extra):
        self.scores[player-1] = self.scores[player-1] + extra   # Score for player 1 goes into position 0, etc.

    def play(self):
        if self.marbles < 40:                               # For quick games, print the board after every move.
            self.board.print_board(self.turn)

        while self.board.last_marble < self.marbles:
            self.next_player()                              # Next player, picks up next marble.

            if (self.board.last_marble % 23) == 0:          # If the next marble to played is a multiple of 23.
                self.add_to_score(self.turn, self.board.last_marble)      # Add marble to their score.
                self.board.counter_clockwise_7()                          # Move 7 places counter-clockwise.

                # Add that marble to their score.
                self.add_to_score(self.turn, self.board.circle[self.board.current_marble])
                self.board.remove_marble()                                # Remove the marble at that position.

            else:                                                         # Normal rules.
                self.board.clockwise()
                self.board.insert_marble()

            if self.marbles < 40:                           # For quick games, print the board after every move.
                self.board.print_board(self.turn)
            else:                                           # For long games, print a progress percentage.
                if (self.board.last_marble % 10000) == 0:
                    print("Percentage complete = %d" % (int(100 * self.board.last_marble / self.marbles)))

    def print_results(self):
        print("Players      = %d" % self.players)
        print("Last Marble  = %d" % self.marbles)
        print("High Score   = %d" % max(self.scores))


game1 = Game(9, 25)                # Number of players, number of marbles.
game1.play()
game1.print_results()
