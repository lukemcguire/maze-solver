"""This module provides the main entry point for the maze solver application.

It initializes the graphical window and manages the application's lifecycle.
"""

from graphics import Window


def main() -> None:
    """Entry point of the maze solver application.

    Creates a graphical window and waits for it to be closed.
    """
    win = Window(800, 600)
    win.wait_for_close()


if __name__ == "__main__":
    main()
