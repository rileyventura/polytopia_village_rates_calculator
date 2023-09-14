import pandas
from scipy.stats import multinomial
from string import punctuation
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


def valid_tile_name(tile):
    valid_tiles = ["mo", "fo", "ef", "ff", "cf", "gf", "mm", "mof", "fof", "eff", "fff", "cff", "gff", "mmf"]
    if tile in valid_tiles:
        return True
    return False


def input_tribe():  # Asks for user input, returns the tribe after data validating
    valid_tribes = ["h", "x", "i", "b", "o", "q", "ai", "aq", "v", "k", "c", "z", "l", "e", "y"]

    char = "aa"

    while char not in valid_tribes:
        char = input("Pick a tribe from this selection : h, x, i, b, o, q, ai, aq, v, k, c, z, l, e, y").lower()

    return char.capitalize()


def input_tile():  # Asks for user input, returns the tiles inputted and their proportion
    valid_tiles = ["mo", "fo", "ef", "ff", "cf", "gf", "mm", "mof", "fof", "eff", "fff", "cff", "gff", "mmf"]
    points = punctuation.replace(",", "")
    digits = "123456789"

    global tile_input_list
    tile_input_string = "bla"
    tile_input_list = ["bla"]  # These variables are to quantify what type tiles are being inputted

    global tile_shape
    tile_shape = []
    # These check that the shape is ok and matches the length of the list of tiles

    global tile_distribution
    global tile_distribution_names
    tile_distribution = []
    tile_distribution_names = []  # These are the output result

    while any(x in tile_input_string for x in points) or [i for i in tile_input_list if
                                                          i not in valid_tiles] != [] or len(tile_shape) != n_tiles:

        # While function makes sure that only the "," is separating data and that the data is valid

        tile_input_string = input(
            "Write the tiles in shortform separated by commas (mo, fo, ef, ff, cf, gf, mm): ").replace(
            " ", "")
        tile_input_list = tile_input_string.split(",")
        x = 0
        for terrain in valid_tiles:
            if tile_input_list.count(terrain) != 0:
                tile_distribution.append(tile_input_list.count(terrain))
                tile_distribution_names.append(terrain)
            x += 1

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
        tile_number()
        print(tile_shape, n_tiles, tile_distribution)
        print(any(x in tile_input_string for x in points), [i for i in tile_input_list if
                                                            i not in valid_tiles] != [], len(tile_shape) != n_tiles)


def tile_number():
    global n_tiles
    n_tiles = 0
    for i in range(len(tile_distribution)):
        n_tiles += tile_distribution[i]  # sum of tiles calculated


def pmf(tribe_used):  # Multinomial distribution with x = tile ratios, n = sum of tiles, p = odds of a tile

    # For the pmf to function, the total p=1,
    # So we have to add the remaining odds in a separate value, hence why append 0

    tile_distribution.append(0)

    tile_number()
    tile_odds_close = []
    tile_odds_far = []
    tile_odds_out = []
    for element in tile_distribution_names:  # Tile info 1 has the names of the tiles that were inputted
        element_f = element + "f"
        element_o = element + "o"
        tile_odds_close.append(getattr(tribe_used, element))
        tile_odds_far.append(getattr(tribe_used, element_f))
        tile_odds_out.append(getattr(tribe_used, element_o))
        # Now we have the odds of a type of tile appearing next, 2 tiles and out of a city

    remaining_probability_close, remaining_probability_far, remaining_probability_out = 1, 1, 1

    for index in range(len(tile_odds_out)):
        remaining_probability_close -= tile_odds_close[index]
        remaining_probability_far -= tile_odds_far[index]
        remaining_probability_out -= tile_odds_out[index]

    tile_odds_close.append(remaining_probability_close)
    tile_odds_far.append(remaining_probability_far)
    tile_odds_out.append(remaining_probability_out)

    tile_distribution_names.append("Other probabilities")
    # Now the remaining probability has been added into the table

    # print("tile names", tile_info[1], "tile proportions", tile_info[0], "odds for a tile", tile_odds_close)
    # print(multinomial.pmf(x=tile_info[0], n=n_tiles, p=tile_odds_close))

    tile_odds = [tile_odds_close, tile_odds_far, tile_odds_out]
    print(tile_odds)
    frequency = []

    for element in range(len(tile_odds)):
        frequency.append(round(multinomial.pmf(x=tile_distribution, n=n_tiles, p=tile_odds[element]) * 100, 2))

    odds = [round(frequency[0] / (frequency[1] + frequency[2] + frequency[0]) * 100, 2),
            round(frequency[1] / (frequency[1] + frequency[2] + frequency[0]) * 100, 2),
            round(frequency[2] / (frequency[1] + frequency[2] + frequency[0]) * 100, 2)]

    if n_tiles == 1:  # pmf formula incorrect for n=1 so this is the simple workaround
        odds[0] = tile_odds[0][0]
        odds[1] = tile_odds[1][0]
        odds[2] = tile_odds[2][0]

    if remaining_probability_close == 1:  # Makes sure that there is always at least one positive P for the formula to be valid
        odds[0] = 0
    if remaining_probability_far == 1:
        odds[1] = 0
    if remaining_probability_out == 1:
        odds[2] = 0
    print(tile_distribution)
    print(tile_distribution_names)
    print(odds)


def board_creation():
    # Fog, neighbor, edge, territory

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

        #   Edge case for the first tile
        if row == 9:
            df.iloc[-1, column] = tile_input_list[index]
        else:
            df.iloc[row, column] = tile_input_list[index]

    # Adding the territory tiles to the board

    base_column = 4
    base_row = 0
    index = 0

    while tile_input_list[index] in tile_names and index < len(tile_shape) - 1:

        if tile_shape[index] == "forwards":
            base_row -= 1
        if tile_shape[index] == "right":
            base_column += 1
        if tile_shape[index] == "backwards":
            base_row += 1
        if tile_shape[index] == "left":
            base_column -= 1

        column = base_column
        row = base_row

        column += 1  # Skips the border tile as it in tiles so will skip the while

        border_count = 0
        for col in range(column):
            if df.iloc[row, col] in tile_names:
                border_count += 1

        while column < 10 and df.iloc[row, column] not in tile_names and border_count < 2:
            df.iloc[row, column] = "ter"

            column += 1

            # Useful for the first time
        if base_row == -1:
            base_row = 9

        index += 1

    print(df)


def position_input():
    position = -1

    while n_tiles >= position > 0:
        position = int(input("Position of the tile to analyze"))

    position -= 1

    return position


def find_adjacent_tiles(rowcol):
    adjacent_tiles = []

    if rowcol[1] == 0:
        low_col = 0
    else:
        low_col = rowcol[1] - 1
    if rowcol[1] == 9:
        upp_col = 10
    else:
        upp_col = rowcol[1] + 2
    if rowcol[0] == 0:
        low_row = 0
    else:
        low_row = rowcol[0] - 1
    if rowcol[0] == 9:
        upp_row = 10
    else:
        upp_row = rowcol[0] + 2

    for r in range(low_row, upp_row):
        for c in range(low_col, upp_col):
            adjacent_tiles.append((r, c))

    return adjacent_tiles


def multi_pmf():
    # Finds the coordinates of the tile of interest
    row = 10
    column = 4

    for index in range(len(tile_shape)):
        if tile_shape[index] == "forwards":
            row -= 1
        elif tile_shape[index] == "right":
            column += 1
        elif tile_shape[index] == "backwards":
            row += 1
        elif tile_shape[index] == "left":
            column -= 1

    studied_tile = (row, column)

    adjacent_tiles = find_adjacent_tiles(studied_tile)

    # Finds the relevant neighbors to the tile of studied_tile

    relevant_neighbor = []

    for tile in adjacent_tiles:
        if df.iloc[tile] == "_":
            relevant_neighbor.append(tile)

    # Finds the relevant borders for each neighbor tiles

    relevant_border = []

    for neighbor in relevant_neighbor:
        adjacent_tiles = find_adjacent_tiles(neighbor)

        for tile in adjacent_tiles:
            if df.iloc[tile] in tile_names:
                relevant_border.append(tile)


def main():  # Applies the pmf specific to a tribe and runs the necessary functions before to apply it
    used_tribe = assign_tribe_odds(input_tribe())
    input_tile()

    board_creation()
    pmf(used_tribe)


def assign_tribe_odds(name):
    temp = data.loc[:, name].values.transpose().tolist()
    return tribe(temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9], temp[10],
                 temp[11], temp[12], temp[13], temp[14], temp[15], temp[16], temp[17], temp[18], temp[19], temp[20])


#   Board creation
df = pandas.DataFrame(np.full((10, 10), "_"))

main()
