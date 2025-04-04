"""This module provides the main entry point for the maze solver application.

It initializes the graphical window and manages the application's lifecycle.
"""

from graphics import Window
from maze import Maze


def main() -> None:
    """Entry point of the maze solver application.

    Creates a graphical window and waits for it to be closed.
    """
    num_rows = 15
    num_cols = 20
    margin = 50
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    win = Window(screen_x, screen_y)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win)
    maze.solve()

    win.wait_for_close()


if __name__ == "__main__":
    main()
