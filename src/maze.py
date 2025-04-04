"""This module defines the Maze class, which represents a grid-based maze.

The Maze class is responsible for creating and managing the cells within the maze,
drawing them on a graphical window, and animating the creation process.
"""

import time
from itertools import product

from cell import Cell
from graphics import Window


class Maze:
    """Represents a maze composed of a grid of cells.

    Attributes:
        _x1 (float): The x-coordinate of the top-left corner of the maze.
        _y1 (float): The y-coordinate of the top-left corner of the maze.
        _num_rows (int): The number of rows in the maze.
        _num_cols (int): The number of columns in the maze.
        _cell_size_x (float): The width of each cell in the maze.
        _cell_size_y (float): The height of each cell in the maze.
        _win (Window | None): The graphical window where the maze will be drawn, or None if no window is associated.
        _cells (list[list[Cell]]): A 2D list of Cell objects representing the maze grid.
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
        """
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells: list[list[Cell]] = []
        self._create_cells()

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
        self._animate()

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
