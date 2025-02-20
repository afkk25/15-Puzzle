# Implementation of the h1 heuristic
def h1(state, problem=None):
    """
    h1 heuristic: Counts the number of tiles that are not in their goal positions.
    Returns:
        int: The h1 heuristic value.
    """
    misplaced_tiles = 0
    current = 1
    for row in range(4):
        for col in range(4):
            if row == 3 and col == 3:  # Last cell should be 0 (blank)
                if state.cells[row][col] != 0:
                    misplaced_tiles += 1
            else:
                if state.cells[row][col] != current:
                    misplaced_tiles += 1
                current += 1
    return misplaced_tiles

# Implementation of the h2 heuristic
def h2(state, problem=None):
    """
    h2 heuristic: Calculates the sum of Euclidean distances for each tile from its current position
    to its goal position.
    Returns:
        float: The h2 heuristic value.
    """
    euclidean_distance = 0.0
    current = 1
    for row in range(4):
        for col in range(4):
            if row == 3 and col == 3:  # Last cell should be 0 (blank)
                if state.cells[row][col] != 0:
                    goal_row, goal_col = 3, 3
                    dx = row - goal_row
                    dy = col - goal_col
                    euclidean_distance += (dx ** 2 + dy ** 2) ** 0.5
            else:
                if state.cells[row][col] != current:
                    goal_row, goal_col = divmod(current - 1, 4)
                    dx = row - goal_row
                    dy = col - goal_col
                    euclidean_distance += (dx ** 2 + dy ** 2) ** 0.5
                current += 1
    return euclidean_distance

# Implementation of the h3 heuristic
def h3(state, problem=None):
    """
    h3 heuristic: Computes Manhattan distances, a lower bound on true cost, as it considers minimum moves.
    Returns:
        int: The h3 heuristic value.
    """
    manhattan_distance = 0
    current = 1
    for row in range(4):
        for col in range(4):
            if row == 3 and col == 3:  # Last cell should be 0 (blank)
                if state.cells[row][col] != 0:
                    goal_row, goal_col = 3, 3
                    manhattan_distance += abs(row - goal_row) + abs(col - goal_col)
            else:
                if state.cells[row][col] != current:
                    goal_row, goal_col = divmod(current - 1, 4)
                    manhattan_distance += abs(row - goal_row) + abs(col - goal_col)
                current += 1
    return manhattan_distance


# Implementation of the h4 heuristic
def h4(state, problem=None):
    """
    h4 heuristic: Calculates the number of tiles out of their goal row plus the number of tiles out of their goal column.
    Returns:
        int: The h4 heuristic value.
    """
    out_of_row = 0
    out_of_column = 0
    current = 1
    for row in range(4):
        for col in range(4):
            if row == 3 and col == 3:  # Last cell should be 0 (blank)
                if state.cells[row][col] != 0:
                    out_of_row += 1
                    out_of_column += 1
            else:
                if state.cells[row][col] != current:
                    goal_row, goal_col = divmod(current - 1, 4)
                    if row != goal_row:
                        out_of_row += 1
                    if col != goal_col:
                        out_of_column += 1
                current += 1
    return out_of_row + out_of_column


