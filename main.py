import pandas
from scipy.stats import multinomial
import numpy as np

# Work on vision that you get from mountains
# Work on different tech that you can have and vision it causes
# Water vision

file = "/home/jack/Downloads/poly_rates.csv"  # change name for the file directory
data = pandas.read_csv(file)  # imports the odds of different tribes from a csv


class tribe:
    def __init__(self, mo, fo, ef, ff, cf, gf, mm, mof, fof, eff, fff, cff, gff, mmf, moo, foo, efo, ffo, cfo, gfo,
                 mmo):
        self.mo = mo
        self.fo = fo
        self.ef = ef
        self.ff = ff
        self.cf = cf
        self.gf = gf
        self.mm = mm
        self.mof = mof
        self.fof = fof
        self.eff = eff
        self.fff = fff
        self.cff = cff
        self.gff = gff
        self.mmf = mmf
        self.moo = moo
        self.foo = foo
        self.efo = efo
        self.ffo = ffo
        self.cfo = cfo
        self.gfo = gfo
        self.mmo = mmo


def ask_tribe():  # Asks for user input, returns the tribe after data validating
    valid_tribes = ["h", "x", "i", "b", "o", "q", "ai", "aq", "v", "k", "c", "z", "l", "e", "y"]

    char = "aa"

    while char not in valid_tribes:
        char = input("Pick a tribe from this selection : h, x, i, b, o, q, ai, aq, v, k, c, z, l, e, y").lower()

    return char.capitalize()


def ask_tech(used_tribe):
    if used_tribe == "x":
        organization = input("Do you have organization? y for yes and n for no: ").lower()
        climbing = True
    if used_tribe == "i":
        climbing = input("Do you have climbing? y for yes and n for no: ").lower()
        organization = True
    else:
        organization = input("Do you have organization? y for yes and n for no: ").lower()
        climbing = input("Do you have climbing? y for yes and n for no: ").lower()

    if organization == "y" or True:
        organization = True
    else:
        organization = False
    if climbing == "y" or True:
        climbing = True
    else:
        climbing = False

    return organization, climbing


def assign_tribe_odds(name):
    temp = data.loc[:, name].values.transpose().tolist()
    return tribe(temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9], temp[10],
                 temp[11], temp[12], temp[13], temp[14], temp[15], temp[16], temp[17], temp[18], temp[19], temp[20])


def valid_tile(tile):  # Inputs a string and confirms if it's a legitimate tile name or not
    valid_tiles = ["mo", "fo", "ef", "ff", "cf", "gf", "mm", "mof", "fof", "eff", "fff", "cff", "gff", "mmf"]
    if tile in valid_tiles:
        return True
    return False


def ask_tiles():  # Asks for a user string that outputs a list of the entered tiles

    while True:
        tiles = input(
            "Write the tiles in shortform separated by commas (mo, fo, ef, ff, cf, gf, mm): "
        ).replace(" ", "").split(",")

        if [i for i in tiles if valid_tile(i)]:
            break

    return tiles


def distribution(tiles):  # Creates a list with the distribution of every kind of tile

    valid_tiles = ["mo", "fo", "ef", "ff", "cf", "gf", "mm", "mof", "fof", "eff", "fff", "cff", "gff", "mmf"]
    x = 0
    tile_distribution = []
    for terrain in valid_tiles:
        if tiles.count(terrain) != 0:
            tile_distribution.append(tiles.count(terrain))
        x += 1

    return tile_distribution


def name_distribution(tiles):  # Associates a name to the tile_distribution list

    valid_tiles = ["mo", "fo", "ef", "ff", "cf", "gf", "mm", "mof", "fof", "eff", "fff", "cff", "gff", "mmf"]
    x = 0
    names_tile_distribution = []
    for terrain in valid_tiles:
        if tiles.count(terrain) != 0:
            names_tile_distribution.append(terrain)
        x += 1

    return names_tile_distribution


def ask_shape(tiles):  # Asks user for a shape that the resources will be aligned in

    digits = "123456789"

    while True:
        tile_shape = []
        shape_input_string = input("Write the tile shape clockwise in this format 3L1R2").replace(" ", "").lower()
        direction = "forwards"  # The shape will keep going straight until there is a direction change by a letter

        for letter in shape_input_string:
            if letter in digits:
                for index in range(int(letter)):
                    tile_shape.append(direction)

            if letter == "l":
                if direction == "backwards":
                    direction = "right"
                elif direction == "left":
                    direction = "backwards"
                elif direction == "forwards":
                    direction = "left"
                elif direction == "right":
                    direction = "forwards"

            if letter == "r":
                if direction == "backwards":
                    direction = "left"
                elif direction == "right":
                    direction = "backwards"
                elif direction == "forwards":
                    direction = "right"
                elif direction == "left":
                    direction = "forwards"
        if len(tile_shape) == len(tiles):
            break
    return tile_shape


def ask_position(tiles):
    # Asks the user which tile they want to analyze relative to the position of the entered tiles.

    while True:
        position = int(input("Position of the tile to analyze (starts at 1): "))
        len_tiles = len(tiles)
        if 0 < position <= len_tiles:
            break

    return position


def pmf(specific_tiles_distribution, specific_tiles_name_distribution, tribe_used, tiles):
    # Multinomial distribution with x = tile ratios, n = sum of tiles, p = odds of a tile
    # For the pmf to function, the total p=1
    # So we have to add the remaining odds in a separate value, hence why append 0
    specific_tiles_distribution.append(0)

    tile_odds_close = []
    tile_odds_far = []
    tile_odds_out = []

    # Odds of a type of tile appearing next, 2 tiles and out of a city for a specific tribe
    for element in specific_tiles_name_distribution:
        element_f = element + "f"
        element_o = element + "o"
        tile_odds_close.append(getattr(tribe_used, element))
        tile_odds_far.append(getattr(tribe_used, element_f))
        tile_odds_out.append(getattr(tribe_used, element_o))

    # The remaining probability's goal is to make all the rest that wasn't picked added in the pmf function so that p=1
    remaining_probability_close, remaining_probability_far, remaining_probability_out = 1, 1, 1

    for index in range(len(tile_odds_out)):
        remaining_probability_close -= tile_odds_close[index]
        remaining_probability_far -= tile_odds_far[index]
        remaining_probability_out -= tile_odds_out[index]

    tile_odds_close.append(remaining_probability_close)
    tile_odds_far.append(remaining_probability_far)
    tile_odds_out.append(remaining_probability_out)
    tile_odds = {"close": tile_odds_close, "far": tile_odds_far, "out": tile_odds_out}
    # Remaining probability has been assigned to the tile_odds of all distances

    specific_tiles_name_distribution.append("Other probabilities")
    # Now the remaining probability has been added into the table, this is only so that the user can understand
    # specific_tiles_name_distribution is not used in the pmf function

    frequency = []

    for element in tile_odds:
        frequency.append(
            round(multinomial.pmf(x=specific_tiles_distribution, n=len(tiles), p=tile_odds[element]), 3))
    print(frequency)
    odds = {
        "close": round(frequency[0] / (frequency[1] + frequency[2] + frequency[0]), 3),
        "far": round(frequency[1] / (frequency[1] + frequency[2] + frequency[0]), 3),
        "out": round(frequency[2] / (frequency[1] + frequency[2] + frequency[0]), 3)
    }
    # pmf formula incorrect for n=1 so this is the simple workaround
    if len(tiles) == 1:
        odds["close"] = tile_odds["close"][0]
        odds["far"] = tile_odds["far"][0]
        odds["out"] = tile_odds["out"][0]

    # Makes sure that there is always at least one positive P for the formula to be valid
    if remaining_probability_close == 1:
        odds["close"] = 0
    if remaining_probability_far == 1:
        odds["far"] = 0
    if remaining_probability_out == 1:
        odds["out"] = 0

    print(odds)

    return odds


def add_border_to_board(tile_shape, tiles):
    # Creates the board and use the tile_shape to assign all tiles on the board
    # Fog, neighbor, edge, territory

    #   Board creation
    df = pandas.DataFrame(np.full((10, 10), "_"))

    #   Inserting shape list onto board
    row, column = 10, 4

    for index in range(len(tile_shape)):
        if tile_shape[index] == "forwards":
            row -= 1
        elif tile_shape[index] == "right":
            column += 1
        elif tile_shape[index] == "backwards":
            row += 1
        elif tile_shape[index] == "left":
            column -= 1

        df.iloc[row, column] = tiles[index]

    return df


def add_territories_to_board(tile_shape, board):
    # Adding the territory tiles to the board starting at a base row & column and moving through the entire shape_list

    base_column = 4
    base_row = 10
    index = 0

    # Will try to add the "ter" tile on the right of every single square in tiles
    while index <= len(tile_shape) - 1:

        if tile_shape[index] == "forwards":
            base_row -= 1
        if tile_shape[index] == "right":
            base_column += 1
        if tile_shape[index] == "backwards":
            base_row += 1
        if tile_shape[index] == "left":
            base_column -= 1

        # The +1 skips the border tile to avoid an iteration in the next while function
        column = base_column + 1
        row = base_row

        # A square will become "ter" if the col < 10, if it is not a border, and it's on the same row as a border
        while column < 10 and not valid_tile(board.iloc[row, column]):
            board.iloc[row, column] = "ter"
            column += 1

        index += 1

    print(board)


def find_adjacent_tiles(row_col):
    adjacent_tiles = []

    if row_col[1] == 0:
        low_col = 0
    else:
        low_col = row_col[1] - 1

    if row_col[1] == 9:
        upp_col = 10
    else:
        upp_col = row_col[1] + 2

    if row_col[0] == 0:
        low_row = 0
    else:
        low_row = row_col[0] - 1

    if row_col[0] == 9:
        upp_row = 10
    else:
        upp_row = row_col[0] + 2

    for r in range(low_row, upp_row):
        for c in range(low_col, upp_col):
            adjacent_tiles.append((r, c))

    return adjacent_tiles


def tile_of_interest_coordinates(tile_shape, studied_position):
    # Finds the coordinates of the tile of interest
    row = 10
    column = 4

    for index in range(studied_position):
        if tile_shape[index] == "forwards":
            row -= 1
        elif tile_shape[index] == "right":
            column += 1
        elif tile_shape[index] == "backwards":
            row += 1
        elif tile_shape[index] == "left":
            column -= 1

    return row, column


def find_relevant_neighbor(board, studied_tile):
    # Finds the relevant neighbors to the tile of studied_tile

    adjacent_tiles = find_adjacent_tiles(studied_tile)
    relevant_neighbor = {}

    for tile in adjacent_tiles:
        if board.iloc[tile] == "_":
            relevant_neighbor[tile] = []

    return relevant_neighbor


def find_relevant_border(board, relevant_neighbor):

    for neighbor in relevant_neighbor:
        relevant_border = []
        adjacent_tiles = find_adjacent_tiles(neighbor)

        for tile in adjacent_tiles:
            if valid_tile(board.iloc[tile]):
                relevant_border.append(tile)

        relevant_neighbor[neighbor] = relevant_border

    return relevant_neighbor


def multi_pmf(tribe_used, relevant_neighbor, board):

    pmf_odds = []
    for neighbor in relevant_neighbor.values():
        specific_tiles = []

        for tile in neighbor:
            specific_tiles.append(board.iloc[tile])

        specific_tiles_distribution = distribution(specific_tiles)
        specific_tile_name_distribution = name_distribution(specific_tiles)

        pmf_odds.append(pmf(specific_tiles_distribution, specific_tile_name_distribution, tribe_used, specific_tiles))

    return pmf_odds


def find_final_odds(pmf_odds):
    final_odds = {"close": 1, "far": 1, "out": 1}

    for odds in pmf_odds:
        final_odds["close"] *= (1-odds["close"])
        final_odds["far"] *= (1-odds["far"])
        final_odds["out"] *= (1-odds["out"])

    final_odds["close"] = 1 - final_odds["close"]
    final_odds["far"] = 1 - final_odds["far"]
    final_odds["out"] = 1 - final_odds["out"]

    return final_odds


def main():  # Applies the pmf specific to a tribe and runs the necessary functions before to apply it
    used_tribe = assign_tribe_odds(ask_tribe())
    tiles = ask_tiles()
    tile_shape = ask_shape(tiles)
    board = add_border_to_board(tile_shape, tiles)
    add_territories_to_board(tile_shape, board)

    studied_position = ask_position(tiles)
    studied_tile = tile_of_interest_coordinates(tile_shape, studied_position)
    # Relevant_neighbor is created in this function
    relevant_neighbor = find_relevant_neighbor(board,studied_tile)
    # relevant_neighbor now has every border associated to every neighbor
    relevant_neighbor = find_relevant_border(board, relevant_neighbor)

    pmf_odds = multi_pmf(used_tribe, relevant_neighbor, board)

    print(find_final_odds(pmf_odds))

main()

#print(multinomial.pmf([1,1,0], 2, [0.385, 0.12, 1-0.385 - 0.12]))