""" Day 10, part 1."""
import sys
import time


def read_pipes(filename: str) -> list:
    """ Read pipes from file and return them in a list of lists.

    Args:
        filename (str): The file containing the pipe values.

    Returns:
        list: A list of lists with all the pipes.
    """
    pipes = []
    with open(filename) as file:
        for line in file:
            pipes.append(list(line.rstrip()))
    return pipes

def find_start(pipes: list) -> (int, int):
    """ Find the "S" pipe and return its position.

    Args:
        pipes (list): A list of lists with all the pipes.

    Returns:
        (int, int): The y, x position of the 'S' pipe.
    """
    for idx_y, pipe_line in enumerate(pipes):
        if 'S' in pipe_line:
            return idx_y, pipe_line.index('S')


def count_steps(pipes: list, start: (int, int)) -> int:
    """ Return the steps required to fill the loop from the start.

    Args:
        pipes (list): A list of lists with all the pipes.
        start (int, int): The starting point.

    Returns:
        int: The amount of steps to return to the start.
    """
    height = len(pipes)
    width = len(pipes[0])
    def flood_fill_pipes(x: int, y: int, dir: str) -> int:
        """ Recursively follow the pipes and return the steps required to
        fill the loop from the start.

        Args:
            x (int): The current position's x.
            y (int): The current position's y.
            dir (str): Previous call's direction.
            steps (int): The number of steps at this position.

        Returns:
            int: The amount of steps to return to the start.
        """
        if x == start[1] and y == start[0]:
            return
        else:
            match dir:
                case 'up':
                    if pipes[y][x] == '|':
                        pipes_copy[y][x] = '║'
                        return flood_fill_pipes(x, y-1, 'up')
                    elif pipes[y][x] == 'F':
                        pipes_copy[y][x] = '╔'
                        return flood_fill_pipes(x+1, y, 'right')
                    elif pipes[y][x] == '7':
                        pipes_copy[y][x] = '╗'
                        return flood_fill_pipes(x-1, y, 'left')
                case 'down':
                    if pipes[y][x] == '|':
                        pipes_copy[y][x] = '║'
                        return flood_fill_pipes(x, y+1, 'down')
                    elif pipes[y][x] == 'L':
                        pipes_copy[y][x] = '╚'
                        return flood_fill_pipes(x+1, y, 'right')
                    elif pipes[y][x] == 'J':
                        pipes_copy[y][x] = '╝'
                        return flood_fill_pipes(x-1, y, 'left')
                case 'left':
                    if pipes[y][x] == '-':
                        pipes_copy[y][x] = '═'
                        return flood_fill_pipes(x-1, y, 'left')
                    elif pipes[y][x] == 'F':
                        pipes_copy[y][x] = '╔'
                        return flood_fill_pipes(x, y+1, 'down')
                    elif pipes[y][x] == 'L':
                        pipes_copy[y][x] = '╚'
                        return flood_fill_pipes(x, y-1, 'up')
                case 'right':
                    if pipes[y][x] == '-':
                        pipes_copy[y][x] = '═'
                        return flood_fill_pipes(x+1, y, 'right')
                    elif pipes[y][x] == 'J':
                        pipes_copy[y][x] = '╝'
                        return flood_fill_pipes(x, y-1, 'up')
                    elif pipes[y][x] == '7':
                        pipes_copy[y][x] = '╗'
                        return flood_fill_pipes(x, y+1, 'down')
    pipes_copy = [row.copy() for row in pipes]
    y, x = start
    if y-1 >= 0 and pipes[y-1][x] in ['|', 'F', '7']:
        flood_fill_pipes(x, y-1, 'up')
    elif y+1 <= height-1 and pipes[y+1][x] in ['|', 'L', 'J']:
        flood_fill_pipes(x, y+1, 'down')
    elif x-1 >= 0 and pipes[y][x-1] in ['-', 'F', 'L']:
        flood_fill_pipes(x-1, y, 'left')
    elif x+1 <= width-1 and pipes[y][x+1] in ['-', 'J', '7']:
        flood_fill_pipes(x+1, y, 'right')

    return pipes_copy

def flip_in_out(in_out: str) -> str:
    return "in" if in_out == "out" else "out" 

def clean_outside(pipes: list, start: list) -> list:
    old = {'.', '|', 'L', 'F', '7', 'J', '-'}
    in_out = "out"
    open_close_down = "closed"
    open_close_up = "closed"
    for y in range(len(pipes)):
        for x in range(len(pipes[y])):
            if pipes[y][x] in old:
                if in_out == "out":
                    pipes[y][x] = ' '
            elif pipes[y][x] == '║':
                in_out = flip_in_out(in_out)
            elif pipes[y][x] == '╔' and open_close_down == 'closed':
                open_close_down = 'open'
            elif pipes[y][x] == '╚' and open_close_up == 'closed':
                open_close_up = 'open'
            elif pipes[y][x] == '╝':
                if open_close_down == 'open':
                    open_close_down = 'closed'
                    in_out = flip_in_out(in_out)
                elif open_close_up == 'open':
                    open_close_up = 'closed'
            elif pipes[y][x] == '╗':
                if open_close_up == 'open':
                    open_close_up = 'closed'
                    in_out = flip_in_out(in_out)
                elif open_close_down == 'open':
                    open_close_down = 'closed'

    return (pipes)


def count_enclosed(pipes: list) -> int:
    old = {'.', '|', 'L', 'F', '7', 'J', '-'}
    enclosed = 0
    for line in pipes:
        for char in line:
            if char in old:
                enclosed += 1

    return enclosed

if __name__ == '__main__':
    sys.setrecursionlimit(100000000)
    tic = time.perf_counter()
    pipes = read_pipes(sys.argv[1])
    start = find_start(pipes)
    new_pipes = count_steps(pipes, start)
    print("")
    cleaned_pipes = clean_outside(new_pipes, (0,0))
    for line in cleaned_pipes:
        for char in line:
            print(char, end="")
        print("")
    print("Enclosed: ", count_enclosed(cleaned_pipes))
    toc = time.perf_counter()
    print(f"Took {toc - tic:0.4f} seconds")
