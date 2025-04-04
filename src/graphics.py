"""This module provides a graphical window class for the maze solver application.

It uses Tkinter to create and manage a window where the maze and its solution
can be visualized.
"""

from __future__ import annotations

from dataclasses import dataclass
from os import environ
from pathlib import Path
from sys import base_prefix

environ["TCL_LIBRARY"] = str(Path(base_prefix) / "lib" / "tcl8.6")
environ["TK_LIBRARY"] = str(Path(base_prefix) / "lib" / "tk8.6")

from tkinter import BOTH, Canvas, Tk


class Window:
    """Represents a graphical window for the maze solver.

    Attributes:
        __root (Tk): The root Tkinter window.
        __canvas (Canvas): The canvas for drawing graphics.
        __running (bool): Indicates whether the window is running.
    """

    def __init__(self, width: int, height: int) -> None:
        """Initializes the Window object.

        Args:
            width: The width of the window.
            height: The height of the window.
        """
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="gray15", width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self) -> None:
        """Redraws the window and updates the display.

        This method forces the Tkinter window to update its contents,
        ensuring that any changes made to the canvas are visible.
        """
        self.__root.update()
        self.__root.update_idletasks()

    def wait_for_close(self) -> None:
        """Waits for the window to be closed by the user.

        This method enters a loop that continuously redraws the window
        until the user closes it.
        """
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def close(self) -> None:
        """Closes the window.

        Sets the running flag to False, which will cause the
        wait_for_close loop to terminate.
        """
        self.__running = False

    def draw_line(self, line: Line, fill_color: str) -> None:
        """Draws a line on the canvas.

        Args:
            line: The line object to draw.
            fill_color: The color to fill the line with.
        """
        line.draw(self.__canvas, fill_color)


@dataclass
class Point:
    """Represents a point in 2D space.

    Attributes:
        x: The x-coordinate of the point (0 is the left of the screen).
        y: The y-coordinate of the point (0 is the top of the screen).
    """

    x: float  # x = 0 -> left of the screen
    y: float  # y = 0 -> top of the screen


class Line:
    """Represents a line segment in 2D space.

    Attributes:
        p1: A point on one end of the line.
        p2: A point on the other end of the line.
    """

    def __init__(self, p1: Point, p2: Point) -> None:
        """Initializes the Line object.

        Args:
            p1: A point on one end of the line.
            p2: A point on the other end of the line.
        """
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas: Canvas, fill_color: str) -> None:
        """Draws the line on the given canvas.

        Args:
            canvas: The canvas to draw the line on.
            fill_color: The color to fill the line with.
        """
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2)
