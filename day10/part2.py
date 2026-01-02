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

def flood_outside(pipes: list, start: (int, int), mode: str = 'safe') -> None:
    """Flood-fill: replace any contiguous characters in `old` with spaces.

    Args:
        pipes: grid to operate on (list of lists).
        start: unused legacy start coordinate (kept for API compatibility).
        mode: 'safe' prevents corner-cutting when moving diagonally;
              'aggressive' allows diagonal moves without orthogonal checks.
    """
    height = len(pipes)
    width = len(pipes[0])
    old = {'.', '|', 'L', 'F', '7', 'J', '-'}

    def fill_from(sx: int, sy: int) -> None:
        stack = [(sx, sy)]
        while stack:
            x, y = stack.pop()
            if x < 0 or x >= width or y < 0 or y >= height:
                continue
            if pipes[y][x] not in old:
                continue
            pipes[y][x] = ' '
            # 8-neighbour directions (dx, dy)
            neighbours = [
                (0, -1), (0, 1), (-1, 0), (1, 0),
                (-1, -1), (1, -1), (-1, 1), (1, 1),
            ]
            for dx, dy in neighbours:
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= width or ny < 0 or ny >= height:
                    continue
                if pipes[ny][nx] not in old:
                    continue
                # Prevent corner-cutting in 'safe' mode: if moving diagonally
                # and both orthogonal neighbours are non-fillable (i.e. boundaries),
                # then don't allow the diagonal move.
                if mode == 'safe' and dx != 0 and dy != 0:
                    orth1 = pipes[y][nx]
                    orth2 = pipes[ny][x]
                    if orth1 not in old and orth2 not in old:
                        continue
                stack.append((nx, ny))

    # flood from all border cells so any area connected to the outside
    # will be cleared. This avoids relying on a single arbitrary start
    # position which may miss outside regions.
    for x in range(width):
        if pipes[0][x] in old:
            fill_from(x, 0)
        if pipes[height-1][x] in old:
            fill_from(x, height-1)
    for y in range(height):
        if pipes[y][0] in old:
            fill_from(0, y)
        if pipes[y][width-1] in old:
            fill_from(width-1, y)

    return pipes


def follow_path(pipes: list, start: (int, int)) -> int:
    """ Return the steps required to fill the loop from the start.

    Args:
        pipes (list): A list of lists with all the pipes.
        start (int, int): The starting point.

    Returns:
        int: The amount of steps to return to the start.
    """
    height = len(pipes)
    width = len(pipes[0])
    old = {'.', '|', 'L', 'F', '7', 'J', '-'}
    def clean_left_right_up_down(x: int, y: int, dir: str) -> int:
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
                    if pipes[y][x] == '║':
                        # if outside of loop to the left, clean it
                        if pipes[y][x-1] in old:
                            pipes[y][x-1] = ' '
                        return clean_left_right_up_down(x, y-1, 'up')
                    elif pipes[y][x] == '╔':
                        if pipes[y][x-1] in old:
                            pipes[y][x-1] = ' '
                        if pipes[y-1][x] in old:
                            pipes[y-1][x] = ' '
                        if pipes[y-1][x-1] in old:
                            pipes[y-1][x-1] = ' '
                        return clean_left_right_up_down(x+1, y, 'right')
                    elif pipes[y][x] == '╗':
                        return clean_left_right_up_down(x-1, y, 'left')
                case 'down':
                    if pipes[y][x] == '║':
                        if pipes[y][x+1] in old:
                            pipes[y][x+1] = ' '
                        return clean_left_right_up_down(x, y+1, 'down')
                    elif pipes[y][x] == '╚':
                        return clean_left_right_up_down(x+1, y, 'right')
                    elif pipes[y][x] == '╝':
                        if pipes[y][x+1] in old:
                            pipes[y][x+1] = ' '
                        if pipes[y+1][x] in old:
                            pipes[y+1][x] = ' '
                        if pipes[y+1][x+1] in old:
                            pipes[y+1][x+1] = ' '
                        return clean_left_right_up_down(x-1, y, 'left')
                case 'left':
                    if pipes[y][x] == '═':
                        if pipes[y+1][x] in old:
                            pipes[y+1][x] = ' '
                        return clean_left_right_up_down(x-1, y, 'left')
                    elif pipes[y][x] == '╔':
                        return clean_left_right_up_down(x, y+1, 'down')
                    elif pipes[y][x] == '╚':
                        return clean_left_right_up_down(x, y-1, 'up')
                case 'right':
                    if pipes[y][x] == '═':
                        if pipes[y-1][x] in old:
                            pipes[y-1][x] = ' '
                        return clean_left_right_up_down(x+1, y, 'right')
                    elif pipes[y][x] == '╝':    
                        return clean_left_right_up_down(x, y-1, 'up')
                    elif pipes[y][x] == '╗':
                        return clean_left_right_up_down(x, y+1, 'down')
    
    y, x = start
    if y-1 >= 0 and pipes[y-1][x] in ['║', '╔', '╗']:
        clean_left_right_up_down(x, y-1, 'up')
    elif y+1 <= height-1 and pipes[y+1][x] in ['║', '╚', '╝']:
        clean_left_right_up_down(x, y+1, 'down')
    elif x-1 >= 0 and pipes[y][x-1] in ['═', '╔', '╚']:
        clean_left_right_up_down(x-1, y, 'left')
    elif x+1 <= width-1 and pipes[y][x+1] in ['═', '╝', '╗']:
        clean_left_right_up_down(x+1, y, 'right')

    return pipes

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
    enclosed_pipes = flood_outside(new_pipes, (0,0), mode='aggressive')
    cleaned_pipes = follow_path(enclosed_pipes, start)
    for line in cleaned_pipes:
        for char in line:
            print(char, end="")
        print("")
    print("Enclosed: ", count_enclosed(cleaned_pipes))
    toc = time.perf_counter()
    print(f"Took {toc - tic:0.4f} seconds")
