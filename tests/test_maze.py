import pytest
from unittest.mock import MagicMock

from maze import Maze
from graphics import Window


def test_maze_create_cells():
    """Tests that the _create_cells method creates the correct number of cells."""
    num_rows = 5
    num_cols = 3
    maze = Maze(0, 0, num_rows, num_cols, 10, 10)
    assert len(maze._cells) == num_rows
    for row in maze._cells:
        assert len(row) == num_cols


def test_maze_draw_cell():
    """Tests that the _draw_cell method calls the draw method of a cell with the correct arguments."""
    num_rows = 2
    num_cols = 2
    cell_size_x = 10
    cell_size_y = 10
    mock_win = MagicMock(spec=Window)
    maze = Maze(50, 50, num_rows, num_cols, cell_size_x, cell_size_y, mock_win)

    # Check that the draw method was called for each cell
    for i in range(num_rows):
        for j in range(num_cols):
            x1 = 50 + j * cell_size_x
            y1 = 50 + i * cell_size_y
            x2 = x1 + cell_size_x
            y2 = y1 + cell_size_y
            maze._cells[i][j].draw = MagicMock()
            maze._draw_cell(i, j)
            maze._cells[i][j].draw.assert_called_once_with(x1, y1, x2, y2)


def test_maze_draw_cell_no_window():
    """Tests that _draw_cell does nothing when no window is provided."""
    num_rows = 2
    num_cols = 2
    cell_size_x = 10
    cell_size_y = 10
    maze = Maze(50, 50, num_rows, num_cols, cell_size_x, cell_size_y)

    # Check that the draw method was not called for each cell
    for i in range(num_rows):
        for j in range(num_cols):
            maze._cells[i][j].draw = MagicMock()
            maze._draw_cell(i, j)
            maze._cells[i][j].draw.assert_not_called()


def test_maze_animate():
    """Tests that the _animate method calls redraw on the window."""
    mock_win = MagicMock(spec=Window)
    maze = Maze(0, 0, 2, 2, 10, 10, mock_win)
    mock_win.reset_mock()
    maze._animate()
    mock_win.redraw.assert_called_once()


def test_maze_animate_no_window():
    """Tests that _animate does nothing when no window is provided."""
    maze = Maze(0, 0, 2, 2, 10, 10)
    maze._animate()
    # No error should be raised, and no method should be called


def test_maze_init_no_window():
    """Tests that a maze can be initialized without a window."""
    maze = Maze(0, 0, 2, 2, 10, 10)
    assert maze._win is None
    assert len(maze._cells) == 2
    for row in maze._cells:
        assert len(row) == 2


def test_break_entrance_and_exit():
    """Tests that _break_entrance_and_exit removes the correct walls."""
    num_rows = 3
    num_cols = 4
    mock_win = MagicMock(spec=Window)
    maze = Maze(0, 0, num_rows, num_cols, 10, 10, mock_win)

    # Check initial state
    assert maze._cells[0][0].has_left_wall is True
    assert maze._cells[num_rows - 1][num_cols - 1].has_right_wall is True

    maze._break_entrance_and_exit()

    # Check that the walls have been removed
    assert maze._cells[0][0].has_left_wall is False
    assert maze._cells[num_rows - 1][num_cols - 1].has_right_wall is False


def test_break_entrance_and_exit_draw_called():
    """Tests that _break_entrance_and_exit calls _draw_cell on the correct cells."""
    num_rows = 3
    num_cols = 4
    mock_win = MagicMock(spec=Window)
    maze = Maze(0, 0, num_rows, num_cols, 10, 10, mock_win)
    maze._draw_cell = MagicMock()

    maze._break_entrance_and_exit()

    # Check that _draw_cell was called on the entrance and exit cells
    maze._draw_cell.assert_any_call(0, 0)
    maze._draw_cell.assert_any_call(num_rows - 1, num_cols - 1)
    assert maze._draw_cell.call_count == 2
