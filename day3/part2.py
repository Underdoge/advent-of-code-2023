""" Day 3, part 2. """

def read_schematic(filename: str) -> list:
    """ Read the input file and return a matrix with the info.

    Args:
        filename (str): The filename.

    Returns:
        list: The matrix containing the info.
    """
    matrix = []
    with open(filename) as file:
        for line in file:
            symbols = [*str(line.rstrip())]
            matrix.append(symbols)
    return matrix


def is_gear_ratio(matrix: list, x: int, y: int) -> tuple:
    """ Check for an adjacent '*' symbol and return its location.

    Args:
        matrix (list): Matrix containing numbers and symbols.
        x (int): The x coordinate.
        y (int): The y coordinate.

    Returns:
        tuple: A tuple with the adjacent '*' symbol coordinate.
    """
    gear_ratio_location = ()
    if matrix[y-1][x-1] == "*":
        gear_ratio_location = (y-1, x-1)
    elif matrix[y-1][x] == "*":
        gear_ratio_location = (y-1, x)
    elif x+1 < len(matrix[0]) and matrix[y-1][x+1] == "*":
        gear_ratio_location = (y-1, x+1)
    elif y+1 < len(matrix) and matrix[y+1][x-1] == "*":
        gear_ratio_location = (y+1, x-1)
    elif y+1 < len(matrix) and matrix[y+1][x] == "*":
        gear_ratio_location = (y+1, x)
    elif x+1 < len(matrix[0]) and y+1 < len(matrix) and (
        matrix[y+1][x+1] == "*"):
        gear_ratio_location = (y+1, x+1)
    elif x+1 < len(matrix[0]) and matrix[y][x+1] == "*":
        gear_ratio_location = (y, x+1)
    elif matrix[y][x-1] == "*":
        gear_ratio_location = (y, x-1)
    return gear_ratio_location


def sum_gear_ratios(matrix: list) -> int:
    """ Traverse through the schematic and add numbers adjacent to symbols.

    Args:
        matrix (list): Matrix containing the symbols and part numbers.

    Returns:
        sum (int): The sum of all part numbers.
    """
    sum = 0
    number = []
    numbers_and_gears = {}
    gear_ratio = False
    for y in range(len(matrix[0])):
        for x in range(len(matrix)):
            if matrix[y][x].isdigit():
                number.append(matrix[y][x])
                if not gear_ratio and is_gear_ratio(matrix, x, y) != ():
                    (gear_x, gear_y) = is_gear_ratio(matrix, x, y)
                    gear_ratio = True
            elif len(number) > 0:
                if gear_ratio:
                    if (gear_x, gear_y) in numbers_and_gears:
                        sum += numbers_and_gears[(gear_x, gear_y)]*int(
                                "".join(number))
                    else:
                        numbers_and_gears[(gear_x, gear_y)] = int(
                            "".join(number))
                    gear_ratio = False
                number = []
    return sum


if __name__ == '__main__':
    print(sum_gear_ratios(read_schematic("input.txt")))
