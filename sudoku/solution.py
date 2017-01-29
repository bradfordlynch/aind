assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Run through all units looking for naked twins
    for unit in unit_list:
        pairs = []

        # Find all instances of naked twins within the unit
        for i in range(len(unit)-1):
            box_vals = values[unit[i]]
            if len(box_vals) == 2:
                # Check for naked twins
                for j in range(i+1, len(unit)):
                    if box_vals == values[unit[j]]:
                        pairs.append((unit[i], unit[j]))
            else:
                # Not of length two, don't check
                pass

        # Eliminate the naked twins as possibilities from their peers
        for pair in pairs:
            vals_to_remove = values[pair[0]]
            for val in vals_to_remove:
                for box in unit:
                    if box not in pair:
                        new_value = values[box].replace(val, '')
                        values = assign_value(values, box, new_value)

    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [[r+c for r,c in zip(rows, cols)], [r+c for r,c in zip(rows, cols[::-1])]]
unit_list = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    empty_vals = '123456789'

    for val in grid:
        # If the box is blank fill it with all possibilities, else the value
        if val == '.':
            values.append(empty_vals)
        else:
            values.append(val)

    # Return a dict mapping the box name to its value(s)
    return dict(zip(cross(rows, cols), values))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    # Get the max width of any column
    width = max(len(values[box]) for box in values ) + 1
    line = '+'.join(['-'*width*3]*3)

    # Print out rows
    for r in rows:
        row_text = ''
        # Append box values to row
        for c in cols:
            row_text += values[r+c].center(width)
            # Add column spacer if after col 3 or 6
            if c in '36':
                row_text += '|'

        print(row_text)

        # Print line row if at rows C or F
        if r in 'CF':
            print(line)

def eliminate(values):
    '''
    Runs through all boxes in values. If a box has a single value, that value is
    removed from all of its peers.
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        Dictionary of the sudoku with eliminate applied
    '''
    # Get single valued boxes
    sngl_val_boxes = [box for box in values if len(values[box]) == 1]
    for box in sngl_val_boxes:
        for peer in peers[box]:
            new_value = values[peer].replace(values[box], '')
            assign_value(values, peer, new_value)

    return values

def only_choice(values):
    '''
    Runs through all units and if a digit shows up in only one box then the
    value of that box is set to that digit.
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        Dictionary of the sudoku with only choice applied
    '''
    # Run through all units
    for unit in unit_list:
        for digit in '123456789':
            boxes_w_digit = [box for box in unit if digit in values[box]]
            if len(boxes_w_digit) == 1:
                assign_value(values, boxes_w_digit[0], digit)

    return values


def reduce_puzzle(values):
    '''
    Iteratively applies eliminate() and only_choice(). If a solution is found,
    it is returned. If a box is found to have no solutions, False
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        If a solution is found: Dictionary of the solved sudoku
        If no progress is made: Dictionary of the unsolved soduku
        If no valid solution exists: False
    '''
    # Check the number of solved boxes in order to track progress
    solved_boxes = [box for box in values if len(values[box]) == 1]
    stop = False

    while not stop:
        # Count the number of solved boxes before applying eliminate and only_choice
        solved_before = len([box for box in values if len(values[box]) == 1])

        # Apply eliminate
        values = eliminate(values)

        # Apply only_choice
        values = only_choice(values)

        # Apply naked twins
        #values = naked_twins(values)

        # Count the number of solved boxes now
        solved_after = len([box for box in values if len(values[box]) == 1])

        # Check progress and stop if stalled
        stop = solved_after == solved_before

        # Check if solution is invalid
        if len([box for box in values if len(values[box]) == 0]):
            return False

    # Once complete, return values
    return values


def search(values):
    '''
    Traverse a tree using depth-first search to solve the sudoku
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        If a solution is found: Dictionary of the solved sudoku
        If no valid solution exists: False
    '''
    # Attempt to solve the puzzle
    reduced = reduce_puzzle(values)

    # If attempt failed, return False
    if reduced is False:
        return False
    else:
        # Aggregate the unsolved boxes
        unsolved = [box for box in reduced if len(reduced[box]) > 1]

        # If all boxes are solved then return the solution
        if len(unsolved) == 0:
            return reduced
        else:
            # Pick one of the boxes with the fewest remaining options
            box_loc = ''
            box_n = 10

            for box in unsolved:
                if len(reduced[box]) < box_n:
                    box_loc = box
                    box_n = len(reduced[box])

            # Pick values from the remaining options for the box and try them
            for digit in reduced[box_loc]:
                new_values = values.copy()
                new_values[box_loc] = digit
                attempt = search(new_values)
                if attempt:
                    return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    assert len(grid) == 81, 'Grid must be of length 81, representing a 9x9 grid'

    # Convert grid to dict representation
    values = grid_values(grid)

    # Apply search
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
