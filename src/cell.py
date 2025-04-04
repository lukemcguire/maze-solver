"""This module defines the Cell class, which represents a single cell within a maze.

Each cell can have walls on its left, right, top, and bottom sides.
The module also provides methods for drawing the cell and its walls
within a graphical window.
"""

from __future__ import annotations

from graphics import Line, Point, Window


class Cell:
    """Represents a cell in the maze.

    Attributes:
        has_left_wall (bool): True if the cell has a left wall, False otherwise.
        has_right_wall (bool): True if the cell has a right wall, False otherwise.
        has_top_wall (bool): True if the cell has a top wall, False otherwise.
        has_bottom_wall (bool): True if the cell has a bottom wall, False otherwise.
        visited (bool): True if the cell has been visited. Starts out False for all cells.
        _x1 (float | None): The x-coordinate of the top-left corner of the cell.
        _y1 (float | None): The y-coordinate of the top-left corner of the cell.
        _x2 (float | None): The x-coordinate of the bottom-right corner of the cell.
        _y2 (float | None): The y-coordinate of the bottom-right corner of the cell.
        _win (Window | None): The window object where the cell will be drawn, or None if no window is associated.
    """

    def __init__(
        self,
        win: Window | None = None,
    ) -> None:
        """Initializes a Cell object.

        Args:
            win: The Window object where the cell will be drawn.
                If None, the cell will not be drawn. Defaults to None.
        """
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self._x1: float | None = None
        self._y1: float | None = None
        self._x2: float | None = None
        self._y2: float | None = None
        self._win = win

    def draw(self, x1: float, y1: float, x2: float, y2: float) -> None:
        """Draws the cell on the window.

        Draws the walls of the cell based on the has_left_wall,
        has_right_wall, has_top_wall, and has_bottom_wall attributes.
        If no window is associated with the cell, this method does nothing.

        Args:
            x1: The x-coordinate of the top-left corner of the cell.
            y1: The y-coordinate of the top-left corner of the cell.
            x2: The x-coordinate of the bottom-right corner of the cell.
            y2: The y-coordinate of the bottom-right corner of the cell.
        """
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        if self._win is None:
            return

        left_wall_color = "snow" if self.has_left_wall else "gray15"
        right_wall_color = "snow" if self.has_right_wall else "gray15"
        top_wall_color = "snow" if self.has_top_wall else "gray15"
        bottom_wall_color = "snow" if self.has_bottom_wall else "gray15"

        self._win.draw_line(Line(Point(x1, y1), Point(x1, y2)), left_wall_color)
        self._win.draw_line(Line(Point(x2, y1), Point(x2, y2)), right_wall_color)
        self._win.draw_line(Line(Point(x1, y1), Point(x2, y1)), top_wall_color)
        self._win.draw_line(Line(Point(x1, y2), Point(x2, y2)), bottom_wall_color)

    def draw_move(self, to_cell: Cell, undo: bool = False) -> None:
        """Draws a line representing a move from this cell to another cell.

        The line is drawn from the center of this cell to the center of the
        `to_cell`. The color of the line indicates whether the move is being
        undone. If no window is associated with the cell, this method does nothing.

        Args:
            to_cell: The cell to move to.
            undo: If True, the move is being undone, and the line will be red.
                Otherwise, the line will be SeaGreen1. Defaults to False.

        Raises:
            Exception: If the coordinates of either cell are not defined.
        """
        if self._win is None:
            return
        line_color = "red" if undo else "SeaGreen1"
        if self._x1 is None or self._y1 is None or self._x2 is None or self._y2 is None:
            raise Exception("cell coordinates not defined")
        if to_cell._x1 is None or to_cell._y1 is None or to_cell._x2 is None or to_cell._y2 is None:
            raise Exception("to_cell coordinates not defined")
        p1 = Point((self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2)
        p2 = Point((to_cell._x1 + to_cell._x2) / 2, (to_cell._y1 + to_cell._y2) / 2)
        self._win.draw_line(Line(p1, p2), line_color)
