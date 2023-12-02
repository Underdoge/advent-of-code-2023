""" Day 1, part 1."""

def sum_numbers(line: str) -> int:
    """ Returns the first digit multiplied by 10, added to the last digit.

    Args:
        line (str): The string containing at least one digit.

    Returns:
        int: The sum.
    """
    chars = list(line)
    nums = [x for x in chars if x.isdigit()]
    return int(nums[0])*10+int(nums[-1])

if __name__ == '__main__':
    sum_calibration_vals = 0
    with open('day1/input.txt') as file:
        for line in file:
            sum_calibration_vals += sum_numbers(line)
    print(sum_calibration_vals)
