# fifteenpuzzle.py
import search
import random
import heuristics

# Module Classes
class FifteenPuzzleState:
    """
    The Fifteen Puzzle.
    """

    def __init__(self, numbers):
        """
        Constructs a new fifteen puzzle from an ordering of numbers.

        numbers: a list of integers from 0 to 15 representing an
          instance of the fifteen puzzle. 0 represents the blank
          space. Thus, the list

            [1, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

          represents the eight puzzle:
            ---------------------
            | 01 |    | 02 | 03 |
            ---------------------
            | 04 | 05 | 06 | 07 |
            ---------------------
            | 08 | 09 | 10 | 11 |
            ---------------------
            | 12 | 13 | 14 | 15 |
            ---------------------

        The configuration of the puzzle is stored in a 2-dimensional
        list (a list of lists) 'cells'.
        """
        #start task
        self.cells = []
        numbers = numbers[:]  # Make a copy
        numbers.reverse()

        #===== Start Change Task 1 =====*/
        for row in range(4):
            self.cells.append([])
            for col in range(4):
                self.cells[row].append(numbers.pop())
                if self.cells[row][col] == 0:
                    self.blankLocation = row, col
        #===== End Change Task 1 =====*/

    def isGoal(self):
        """
        Checks to see if the puzzle is in its goal state
        (blank in bottom right).

        """
        #===== Start Change Task 1 =====*/
        current = 1
        for row in range(4):
            for col in range(4):
                if row == 3 and col == 3:  # Bottom right
                    if self.cells[row][col] != 0:
                        return False
                else:
                    if current != self.cells[row][col]:
                        return False
                current += 1
        return True
        #===== End Change Task 1 =====*/

    def legalMoves(self):
        """
        Returns a list of legal moves from the current state.
        """
        moves = []
        row, col = self.blankLocation
        if row != 0:
            moves.append('up')

        #===== Start Change Task 1 =====*/
        if row != 3:
            moves.append('down')
        #===== End Change Task 1 =====*/

        if col != 0:
            moves.append('left')

        #===== Start Change Task 1 =====*/
        if col != 3:
            moves.append('right')
        #===== End Change Task 1 =====*/

        return moves
        

    def result(self, move):
        """
        Returns a new fifteenPuzzle with the current state and blankLocation
        updated based on the provided move.
        """
        row, col = self.blankLocation
        if move == 'up':
            newrow = row - 1
            newcol = col
        elif move == 'down':
            newrow = row + 1
            newcol = col
        elif move == 'left':
            newrow = row
            newcol = col - 1
        elif move == 'right':
            newrow = row
            newcol = col + 1
        else:
            raise "Illegal Move"

        # Create a copy of the current fifteenPuzzle

        #===== Start Change Task 1 =====*/
        newPuzzle = FifteenPuzzleState([0] * 16) # 16 since it is a puzzle of 15
        #===== End Change Task 1 =====*/

        newPuzzle.cells = [values[:] for values in self.cells]

        # And update it to reflect the move
        newPuzzle.cells[row][col] = self.cells[newrow][newcol]
        newPuzzle.cells[newrow][newcol] = self.cells[row][col]
        newPuzzle.blankLocation = newrow, newcol
        return newPuzzle

    def __eq__(self, other):
        """
            Overloads '==' such that two fifteenPuzzles with the same configuration
         are equal.

        >>> FifteenPuzzleState([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]) == \
              FifteenPuzzleState([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0, 15]).result('right')
          True
        """
        #===== Start Change Task 1 =====*/
        for row in range(4):
            if self.cells[row] != other.cells[row]:
                return False
        return True
        #===== End Change Task 1 =====*/

    def __hash__(self):
        return hash(str(self.cells))

    def ____getAsciiString(self):
        """
        Returns a display string for the maze
        """
        #===== Start Change Task 1 =====*/
        # The display was adjusted accordingly to display 15 puzzle
        lines = []
        horizontalLine = ('-' * (17))
        lines.append(horizontalLine)
        for row in self.cells:
            rowLine = '|'
            for col in row:
                if col == 0:
                    val = ' '
                else:
                    val = str(col)
                rowLine = rowLine + ' ' + val.ljust(2) + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)
        #===== End Change Task 1 =====*/

    def __str__(self):
        return self.____getAsciiString()

# TODO: Implement The methods in this class
class FifteenPuzzleSearchProblem(search.SearchProblem):
    """
    Implementation of a SearchProblem for the Fifteen Puzzle domain
    Each state is represented by an instance of a fifteenPuzzle.
    """

    def __init__(self, puzzle):
        "Creates a new FifteenPuzzleSearchProblem which stores search information."
        self.puzzle = puzzle

    def getStartState(self):
        return self.puzzle

    def isGoalState(self, state):
        return state.isGoal()

    def getSuccessors(self, state):
        """
        Returns list of (successor, action, stepCost) pairs where
        each successor is either left, right, up, or down
        from the original state and the cost is 1.0 for each
        """
        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a, 1))
        return succ

    def getCostOfActions(self, actions):
        """
        actions: A list of actions to take
        This method returns the total cost of a particular sequence of actions. The sequence must
        be composed of legal moves
        """
        return len(actions)


FIFTEEN_PUZZLE_DATA = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 0, 14],
    [4, 3, 2, 7, 0, 5, 1, 6, 8, 9, 10, 11, 12, 13, 14, 15],
    [5, 1, 3, 4, 0, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [1, 2, 5, 7, 6, 8, 0, 4, 3, 9, 10, 11, 12, 13, 14, 15],
    [0, 3, 1, 6, 8, 2, 7, 5, 4, 9, 10, 11, 12, 13, 14, 15]
]

def loadFifteenPuzzle(puzzleNumber):
    """
    puzzleNumber: The number of the fifteen puzzle to load.
    Returns a fifteen puzzle object generated from one of the
    provided puzzles in FIFTEEN_PUZZLE_DATA.
    puzzleNumber can range from 0 to 5.
    >>> print loadEightPuzzle(1)
        ---------------------
        | 01 | 02 | 03 | 04 |
        ---------------------
        | 05 | 06 | 07 | 08 |
        ---------------------
        | 09 | 10 | 11 | 12 |
        ---------------------
        | 13 | 15 | 00 | 14 |
        ---------------------
    """
    return FifteenPuzzleState(FIFTEEN_PUZZLE_DATA[puzzleNumber])

def createRandomFifteenPuzzle(moves=100):
    """
    moves: number of random moves to apply
    Creates a random fifteen puzzle by applying
    a series of 'moves' random moves to a solved
    puzzle.
    """
    #===== Start Change Task 1 =====*/
    puzzle = FifteenPuzzleState([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0])  # Solved state
    #===== End Change Task 1 =====*/

    for _ in range(moves):
        puzzle = puzzle.result(random.sample(puzzle.legalMoves(), 1)[0])
    return puzzle

if __name__ == '__main__':
    #===== Start Change Task 1 =====*/
    print("Hello, this is the 15-Puzzle game")

    while True:
        print("\nSelect a heuristic function:")
        print("1. h1 (Misplaced Tiles)")
        print("2. h2 (Euclidean distance)")
        print("3. h3 (Manhattan distance)")
        print("4. h4 (Out of row + Out of column)")
        print("5. Quit")

        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == '1':
            heuristic = heuristics.h1
        elif choice == '2':
            heuristic = heuristics.h2
        elif choice == '3':
            heuristic = heuristics.h3
        elif choice == '4':
            heuristic = heuristics.h4
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2,3,4 or 5.")
            continue

        puzzle = createRandomFifteenPuzzle(25)
        print('A random puzzle:')
        print(puzzle)

        problem = FifteenPuzzleSearchProblem(puzzle)
        path = search.aStarSearch(problem, heuristic=heuristic)

        if path:
            print('A* with the selected heuristic found a path of %d moves: %s' % (len(path), str(path)))
        else:
            print('no result.')

        curr = puzzle
        i = 1
        for a in path:
            curr = curr.result(a)
            print('After %d move%s: %s' % (i, ("", "s")[i > 1], a))
            print(curr)

            input("Click return for the next state...")  
            i += 1

        #===== End Change Task 1 =====*/