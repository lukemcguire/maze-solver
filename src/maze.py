"""This module defines the Maze class, which represents a grid-based maze.

The Maze class is responsible for creating and managing the cells within the maze,
drawing them on a graphical window, and generating the maze structure using a
recursive backtracking algorithm.
"""

import random
import time
from itertools import product

from cell import Cell
from graphics import Window

DIRECTIONS = [("down", 1, 0), ("right", 0, 1), ("up", -1, 0), ("left", 0, -1)]


class Maze:
    """Represents a maze composed of a grid of cells.

    Attributes:
        _x1 (float): The x-coordinate of the top-left corner of the maze.
        _y1 (float): The y-coordinate of the top-left corner of the maze.
        _num_rows (int): The number of rows in the maze.
        _num_cols (int): The number of columns in the maze.
        _cell_size_x (float): The width of each cell in the maze.
        _cell_size_y (float): The height of each cell in the maze.
        _win (Window | None): The graphical window where the maze will be drawn,
            or None if no window is associated.
        _cells (list[list[Cell]]): A 2D list of Cell objects representing the
            maze grid.
    """

    def __init__(
        self,
        x1: float,
        y1: float,
        num_rows: int,
        num_cols: int,
        cell_size_x: float,
        cell_size_y: float,
        win: Window | None = None,
        seed: int | None = None,
    ) -> None:
        """Initializes a Maze object.

        Args:
            x1: The x-coordinate of the top-left corner of the maze.
            y1: The y-coordinate of the top-left corner of the maze.
            num_rows: The number of rows in the maze.
            num_cols: The number of columns in the maze.
            cell_size_x: The width of each cell in the maze.
            cell_size_y: The height of each cell in the maze.
            win: The graphical window where the maze will be drawn.
                If None, the maze will not be drawn. Defaults to None.
            seed: An optional seed for the random number generator, used for
                reproducible maze generation. Defaults to None.
        """
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells: list[list[Cell]] = []

        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def solve(self) -> bool:
        """Solves the maze using a recursive backtracking algorithm.

        Returns:
            True if a solution is found, False otherwise.
        """
        return self._solve_r(0, 0)

    def _is_valid_move(self, i: int, j: int, dy: int, dx: int) -> bool:
        """Checks if a move to a neighboring cell is valid.

        Args:
            i: The current row index.
            j: The current column index.
            dy: The change in row index.
            dx: The change in column index.

        Returns:
            True if the move is valid, False otherwise.
        """
        new_y, new_x = i + dy, j + dx
        if not (0 <= new_y < self._num_rows and 0 <= new_x < self._num_cols):
            return False
        next_cell = self._cells[new_y][new_x]
        return not next_cell.visited

    def _has_wall_in_direction(self, cell: Cell, direction: str) -> bool:
        """Checks if the current cell has a wall in the given direction.

        Args:
            cell: The current cell.
            direction: The direction to check.

        Returns:
            True if there is a wall in the given direction, False otherwise.

        Raises:
            ValueError: If an invalid direction is supplied as an argument.
        """
        match direction:
            case "up":
                return cell.has_top_wall
            case "down":
                return cell.has_bottom_wall
            case "left":
                return cell.has_left_wall
            case "right":
                return cell.has_right_wall
            case _:
                raise ValueError(f"Invalid direction: {direction}")

    def _solve_r(self, i: int, j: int) -> bool:
        """Recursively solves the maze from a given cell.

        Args:
            i: The row index of the current cell.
            j: The column index of the current cell.

        Returns:
            True if a solution is found from this cell, False otherwise.
        """
        self._animate()
        current_cell = self._cells[i][j]
        current_cell.visited = True

        if i == self._num_rows - 1 and j == self._num_cols - 1:
            return True

        for direction, dy, dx in DIRECTIONS:
            if self._has_wall_in_direction(current_cell, direction):
                continue

            if not self._is_valid_move(i, j, dy, dx):
                continue

            new_y, new_x = i + dy, j + dx
            next_cell = self._cells[new_y][new_x]
            current_cell.draw_move(next_cell)
            if self._solve_r(new_y, new_x):
                return True
            else:
                current_cell.draw_move(next_cell, undo=True)

        return False

    def _create_cells(self) -> None:
        """Creates and draws all cells in the maze.

        Iterates through each cell position in the grid and calls _draw_cell
        to create and draw the cell.
        """
        for _ in range(self._num_rows):
            row = []
            for _ in range(self._num_cols):
                row.append(Cell(self._win))
            self._cells.append(row)

        for i, j in product(range(self._num_rows), range(self._num_cols)):
            self._draw_cell(i, j)

    def _draw_cell(self, i: int, j: int) -> None:
        """Draws a single cell at the specified row and column.

        Calculates the coordinates of the cell based on its position in the grid
        and the cell size, then draws the cell using its draw method.
        If no window is associated with the maze, this method does nothing.

        Args:
            i: The row index of the cell.
            j: The column index of the cell.
        """
        if self._win is None:
            return
        x1 = self._x1 + j * self._cell_size_x
        y1 = self._y1 + i * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        # self._animate()

    def _animate(self) -> None:
        """Animates the drawing of the maze.

        Redraws the window and pauses briefly to create an animation effect.
        If no window is associated with the maze, this method does nothing.
        """
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self) -> None:
        """Breaks the entrance and exit walls of the maze.

        Removes the left wall of the top-left cell to create an entrance,
        and removes the right wall of the bottom-right cell to create an exit.
        Then redraws the cells to reflect the changes.
        """
        # entrance
        self._cells[0][0].has_left_wall = False
        self._draw_cell(0, 0)
        # exit
        m, n = self._num_rows - 1, self._num_cols - 1
        self._cells[m][n].has_right_wall = False
        self._draw_cell(m, n)

    def _break_walls_r(self, i: int, j: int) -> None:
        """Recursively breaks down walls to generate the maze structure.

        This method implements a recursive backtracking algorithm to carve out
        passages in the maze. It starts at a given cell and randomly chooses
        unvisited neighboring cells to move to, breaking down the walls between
        them.

        Args:
            i: The row index of the current cell.
            j: The column index of the current cell.
        """
        current_cell = self._cells[i][j]
        current_cell.visited = True
        while True:
            to_visit = []
            for direction, dy, dx in DIRECTIONS:
                new_y, new_x = i + dy, j + dx
                if (
                    0 <= new_x < self._num_cols
                    and 0 <= new_y < self._num_rows
                    and not self._cells[new_y][new_x].visited
                ):
                    to_visit.append((direction, dy, dx))
            if not to_visit:
                self._draw_cell(i, j)
                return
            # pick a random direction to go
            direction, dy, dx = random.choice(to_visit)
            to_cell = self._cells[i + dy][j + dx]
            match direction:
                case "up":
                    current_cell.has_top_wall = False
                    to_cell.has_bottom_wall = False
                case "down":
                    current_cell.has_bottom_wall = False
                    to_cell.has_top_wall = False
                case "left":
                    current_cell.has_left_wall = False
                    to_cell.has_right_wall = False
                case "right":
                    current_cell.has_right_wall = False
                    to_cell.has_left_wall = False
            self._draw_cell(i, j)
            self._break_walls_r(i + dy, j + dx)

    def _reset_cells_visited(self) -> None:
        """Reset the visited property of all the cells in the Maze to False."""
        for i, j in product(range(self._num_rows), range(self._num_cols)):
            self._cells[i][j].visited = False
