"""This module provides a graphical window class for the maze solver application.

It uses Tkinter to create and manage a window where the maze and its solution
can be visualized.
"""

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
            width (int): The width of the window.
            height (int): The height of the window.
        """
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="gray15", width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self) -> None:
        """Redraws the window and updates the display."""
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
