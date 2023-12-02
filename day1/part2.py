""" Day 1, part 2."""

NUMS = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
        'nine']

def sum_numbers(line: str) -> int:
    """ Returns the first digit multiplied by 10, added to the last digit.

    Args:
        line (str): The string containing at least one digit.

    Returns:
        int: The sum for the 1st digit multiplied by 10, added  to the last
            digit.
    """
    dec = ""
    chars = list(line)
    for x in range(len(line)):
        if chars[x].isdigit():
            dec = chars[x]
            break
        else:
            for letters in [3, 4, 5]:
                if "".join(chars[x:x+letters]) in NUMS:
                    dec = str(NUMS.index("".join(chars[x:x+letters]))+1)
                    break
        if dec != "":
            break
        else:
            x += 1
    x = len(line) - 1
    num = ""
    while x >= 0:
        if chars[x].isdigit():
            num = chars[x]
            break
        else:
            for letters in [3, 4, 5]:
                if "".join(chars[x:x+letters]) in NUMS:
                    num = str(NUMS.index("".join(chars[x:x+letters]))+1)
                    break
        if num != "":
            break
        else:
            x -= 1
    return int(dec)*10+int(num)

if __name__ == '__main__':
    sum_calibration_vals = 0
    with open('input.txt') as file:
        for line in file:
            sum_calibration_vals += sum_numbers(line)
    print(sum_calibration_vals)
