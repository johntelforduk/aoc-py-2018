# This is a solution to the Advent Of Code 2018 puzzle - Day 14
# https://adventofcode.com/2018/day/14

def int_list_to_str(list):                      # Convert a list of integers to a string.
    result = ""
    for i in list:
        result = result + str(i)
    return (result)

class Kitchen:

    def __init__(self, target_pattern):
        self.recipes = []                       # List of recipes created so far.
        self.num_recipes = 0                    # Number of recipes produced so far.\
        self.elves = []                         # List of Elves working in the kitchen.
        self.num_elves = 0                      # Number of elves working in the kitchen.
        self.target_pattern = target_pattern    # The pattern of recipes that the kitchen is looking for.
        self.target_found = False               # Has the target recipe pattern been found yet?
        self.target_found_recipes = 0           # Target pattern found after this many recipes.

    def __str__(self):
        recs = ""
        for r in range(0, self.num_recipes):
            recipe_str = str(self.recipes[r])
            if r == self.elves[0]:                          # Round brackets around 1st elf's current recipe.
                recs = recs + "(" + recipe_str + ")"
            elif r == self.elves[1]:
                recs = recs + "[" + recipe_str + "]"        # Square brackets around 2ns elf's current recipe.
            else:
                recs = recs + " " + recipe_str + " "
        return recs

    def add_recipe(self, new_recipe):
        self.num_recipes = self.num_recipes + 1
        self.recipes.append(new_recipe)

    def add_elf(self, start_recipe):
        self.add_recipe(start_recipe)
        self.elves.append(self.num_recipes - 1)
        self.num_elves = self.num_elves + 1

    def check_target_found(self):
        if self.num_recipes >= len(self.target_pattern) and self.target_found is False:
            last_few_recipes = \
                self.recipes[(self.num_recipes - len(self.target_pattern)) \
                                     :(self.num_recipes + len(self.target_pattern))]

            if self.target_pattern == last_few_recipes:
                self.target_found = True
                self.target_found_recipes = self.num_recipes

    def new_recipe(self):
        rec1 = self.recipes[self.elves[0]]      # 1st elf's current recipe.
        rec2 = self.recipes[self.elves[1]]      # 2nd elf's current recipe.

        new_rec = rec1 + rec2                   # Calculate the new recipte.
        new_rec_div10 = new_rec // 10           # New recipe DIV 10
        new_rec_mod10 = new_rec % 10            # New recipe MOD 10

        if new_rec_div10 > 0:
            self.add_recipe(new_rec_div10)
            self.check_target_found()

        self.add_recipe(new_rec_mod10)
        self.check_target_found()

    def move_elves(self):
        for e in range (0, self.num_elves):
            steps = self.recipes[self.elves[e]] + 1                   # How many steps forwards for this elf.
            self.elves[e] = (self.elves[e] + steps) % self.num_recipes    # Move him that far, looping back if necessary.

practices = 793031
choc_kitchen = Kitchen([7,9,3,0,3,1])       # Create a hot chocolate kitchen, that will look for the parm pattern.

choc_kitchen.add_elf(3)                     # Elf #1 makes recipe 3.
choc_kitchen.add_elf(7)                     # Elf #2 makes recipe 7.

if practices < 50:
    print(choc_kitchen)

p1_done = False
p2_done = False

while p1_done is False or p2_done is False:
    choc_kitchen.new_recipe()
    choc_kitchen.move_elves()

    if practices < 50:
        print (choc_kitchen)
    else:
        if (choc_kitchen.num_recipes % 100000) == 0:
            print ("Num recipes so far : %d" % choc_kitchen.num_recipes)

    # Part 1 of the puzzle.
    if choc_kitchen.num_recipes > (practices + 10) and p1_done is False:
        print ("After %d recipes, the scores of the next ten would be %s." \
        % (practices, int_list_to_str(choc_kitchen.recipes[(practices):(practices + 10)])))
        p1_done = True

    # Part 2 of the puzzle.
    if choc_kitchen.target_found and p2_done is False:
        print ("%s first appears after %d recipes." \
        % (int_list_to_str(choc_kitchen.target_pattern), \
           choc_kitchen.target_found_recipes - len(choc_kitchen.target_pattern)))
        p2_done = True
