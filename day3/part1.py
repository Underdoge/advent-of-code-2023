""" Day 3, part 1. """
import string


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

def adjacent_symbols(matrix: list, x: int, y: int, symbols: list) -> bool:
    """ Check for adjacent symbols.

    Args:
        matrix (list): Matrix containing part numbers and symbols.
        x (int): The x coordinate.
        y (int): The y coordinate.
        symbols (list): A list containing all symbols except '.'.

    Returns:
        bool: True if there's an adjacent symbol.
    """
    return (
        matrix[y-1][x-1] in symbols) or (
        matrix[y-1][x] in symbols) or (
        x+1 < len(matrix[0]) and matrix[y-1][x+1] in symbols) or (
        y+1 < len(matrix) and matrix[y+1][x-1] in symbols) or (
        y+1 < len(matrix) and matrix[y+1][x] in symbols) or (
        x+1 < len(matrix[0]) and y+1 < len(matrix) and (
            matrix[y+1][x+1])) in symbols or (
        x+1 < len(matrix[0]) and matrix[y][x+1] in symbols) or (
        matrix[y][x-1] in symbols)


def sum_part_numbers(matrix: list) -> int:
    """ Traverse through the schematic and add numbers adjacent to symbols.

    Args:
        matrix (list): Matrix containing the symbols and part numbers.

    Returns:
        sum (int): The sum of all part numbers.
    """
    symbols = list(string.punctuation.replace(".",""))
    sum = 0
    number = []
    part_number = False
    for y in range(len(matrix[0])):
        for x in range(len(matrix)):
            if matrix[y][x].isdigit():
                number.append(matrix[y][x])
                if not part_number and adjacent_symbols(matrix, x, y, symbols):
                    part_number = True
            elif len(number) > 0:
                if part_number:
                    sum += int("".join(number))
                    part_number = False
                number = []
    return sum

if __name__ == '__main__':
    print(sum_part_numbers(read_schematic("input.txt")))
