""" Day 9, part 2."""
import time
from operator import countOf


def read_values(filename: str) -> list:
    """ Read history values and return them in a list.

    Args:
        filename (str): The file containing the history values.

    Returns:
        list: A list with all the values.
    """
    history = []
    with open(filename) as file:
        for line in file:
            history.append([int(x) for x in line.rsplit()])
    return history


def previous_value(history: list) -> int:
    """ Return the previous value in the history.

    Args:
        history (list): A list with the history values.

    Returns:
        int: The previous value in the history.
    """
    diffs = []
    diffs.append(history)
    x = 0
    while True:
        diff = []
        for idx, value in enumerate(diffs[x]):
            if idx + 1 < len(diffs[x]):
                diff.append(diffs[x][idx+1] - value)
        if len(diff) > 0:
            diffs.append(diff)
            if countOf(diff, 0) == len(diff):
                y = len(diffs) - 2
                while y >= 0:
                    diffs[y].insert(0, diffs[y][0]-diffs[y+1][0])
                    y -= 1
                return diffs[0][0]
        x += 1


def sum_previous_values(values: list) -> int:
    """ Sum all next values in the histories.

    Args:
        values (list): A list with all the next values.

    Returns:
        int: The sum of all next values.
    """
    sum = 0
    for history in values:
        sum += previous_value(history)
    return sum


if __name__ == '__main__':
    tic = time.perf_counter()
    values = read_values("input.txt")
    print("Sum of previous values:", sum_previous_values(values))
    toc = time.perf_counter()
    print(f"Took {toc - tic:0.4f} seconds")
