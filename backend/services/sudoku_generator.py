import random

class SudokuGenerator:
    def __init__(self):
        self.grid_size = 9
        self.subgrid_size = 3

    def generate_sudoku(self):
        """Generates a valid Sudoku puzzle and its solution."""
        solution = self._generate_solution()
        puzzle = self._remove_numbers(solution)
        return puzzle, solution

    def validate_sudoku(self, puzzle, solution):
        """Validates that the puzzle and solution are correct."""
        if not self._is_valid_grid(puzzle) or not self._is_valid_grid(solution):
            return False

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if puzzle[row][col] != 0 and puzzle[row][col] != solution[row][col]:
                    return False

        return self._is_valid_solution(solution) and self._is_valid_solution(puzzle)

    def _generate_solution(self):
        """Generates a complete valid Sudoku solution."""
        grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self._fill_grid(grid)
        return grid

    def _fill_grid(self, grid):
        """Fills the grid with a valid Sudoku solution."""
        def is_valid_placement(grid, row, col, num):
            # Check row
            if num in grid[row]:
                return False

            # Check column
            if num in [grid[r][col] for r in range(self.grid_size)]:
                return False

            # Check subgrid
            start_row, start_col = row - row % self.subgrid_size, col - col % self.subgrid_size
            for r in range(start_row, start_row + self.subgrid_size):
                for c in range(start_col, start_col + self.subgrid_size):
                    if grid[r][c] == num:
                        return False

            return True

        def solve(grid):
            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    if grid[row][col] == 0:
                        for num in range(1, self.grid_size + 1):
                            if is_valid_placement(grid, row, col, num):
                                grid[row][col] = num
                                if solve(grid):
                                    return True
                                grid[row][col] = 0
                        return False
            return True

        solve(grid)

    def _remove_numbers(self, grid):
        """Removes numbers from the grid to create a solvable puzzle."""
        puzzle = [row[:] for row in grid]
        cells_to_remove = random.randint(40, 60)  # Number of cells to remove

        for _ in range(cells_to_remove):
            row, col = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            while puzzle[row][col] == 0:  # Ensure we don't remove the same cell twice
                row, col = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            puzzle[row][col] = 0

        return puzzle

    def _is_valid_grid(self, grid):
        """Checks if the grid is valid (9x9 with numbers 0-9)."""
        if len(grid) != self.grid_size or any(len(row) != self.grid_size for row in grid):
            return False

        for row in grid:
            for num in row:
                if num < 0 or num > 9:
                    return False

        return True

    def _is_valid_solution(self, grid):
        """Checks if the solution is valid according to Sudoku rules."""
        return self._check_rows(grid) and self._check_columns(grid) and self._check_subgrids(grid)

    def _check_rows(self, grid):
        """Checks if all rows are valid."""
        for row in grid:
            if not self._check_unique(row):
                return False
        return True

    def _check_columns(self, grid):
        """Checks if all columns are valid."""
        for col in range(self.grid_size):
            column = [grid[row][col] for row in range(self.grid_size)]
            if not self._check_unique(column):
                return False
        return True

    def _check_subgrids(self, grid):
        """Checks if all subgrids are valid."""
        for row in range(0, self.grid_size, self.subgrid_size):
            for col in range(0, self.grid_size, self.subgrid_size):
                subgrid = [
                    grid[r][c]
                    for r in range(row, row + self.subgrid_size)
                    for c in range(col, col + self.subgrid_size)
                ]
                if not self._check_unique(subgrid):
                    return False
        return True

    def _check_unique(self, numbers):
        """Checks if numbers contain unique non-zero values."""
        nums = [num for num in numbers if num != 0]
        return len(nums) == len(set(nums))
