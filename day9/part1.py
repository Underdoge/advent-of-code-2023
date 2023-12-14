""" Day 9, part 1."""
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

def next_value(history: list) -> int:
    """ Return the next value in the history.

    Args:
        history (list): A list with the history values.

    Returns:
        int: The next value in the history.
    """
    diffs = []
    result = 0
    diffs.append(history)
    x = 0
    while result == 0:
        diff = []
        for idx, value in enumerate(diffs[x]):
            if idx + 1 < len(diffs[x]):
                diff.append(diffs[x][idx+1] - value)
        if len(diff) > 0:
            diffs.append(diff)
            if countOf(diff, 0) == len(diff):
                y = len(diffs) - 2
                while y >= 0:
                    diffs[y].append(diffs[y][-1]+diffs[y+1][-1])
                    y -= 1
                result = diffs[0][-1]
        x += 1
    return result


def sum_extrapolated_values(values: list) -> int:
    """ Sum all next values in the histories.

    Args:
        values (list): A list with all the next values.

    Returns:
        int: The sum of all next values.
    """
    sum = 0
    for history in values:
        sum += next_value(history)
    return sum


if __name__ == '__main__':
    tic = time.perf_counter()
    values = read_values("input.txt")
    print("Sum of extrapolated values:", sum_extrapolated_values(values))
    toc = time.perf_counter()
    print(f"Took {toc - tic:0.4f} seconds")
