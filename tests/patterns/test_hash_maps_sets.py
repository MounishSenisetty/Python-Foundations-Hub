"""Tests for the ``patterns.hash_maps_sets`` modules."""

from typing import List

from patterns.hash_maps_sets.pair_sum_unsorted import pair_sum_unsorted
from patterns.hash_maps_sets.verify_sudoku_board import verify_sudoku_board
from patterns.hash_maps_sets.zero_striping import set_matrix_zeros


def _empty_board() -> List[List[int]]:
    return [[0] * 9 for _ in range(9)]


class TestPairSumUnsorted:
    def test_finds_pair(self) -> None:
        assert pair_sum_unsorted([2, 7, 11, 15], 9) == (0, 1)

    def test_unsorted_input(self) -> None:
        assert pair_sum_unsorted([3, 2, 4], 6) == (1, 2)

    def test_no_pair_returns_none(self) -> None:
        assert pair_sum_unsorted([1, 2, 3], 100) is None

    def test_duplicate_values(self) -> None:
        assert pair_sum_unsorted([3, 3], 6) == (0, 1)

    def test_empty_and_single(self) -> None:
        assert pair_sum_unsorted([], 0) is None
        assert pair_sum_unsorted([1], 1) is None

    def test_negatives(self) -> None:
        assert pair_sum_unsorted([-1, -2, -3, -4], -6) == (1, 3)


class TestVerifySudokuBoard:
    def test_empty_board_is_valid(self) -> None:
        assert verify_sudoku_board(_empty_board()) is True

    def test_valid_partial_board(self) -> None:
        board = _empty_board()
        board[0][0], board[0][1], board[1][0] = 5, 3, 6
        assert verify_sudoku_board(board) is True

    def test_duplicate_in_row(self) -> None:
        board = _empty_board()
        board[0][0], board[0][5] = 4, 4
        assert verify_sudoku_board(board) is False

    def test_duplicate_in_column(self) -> None:
        board = _empty_board()
        board[0][0], board[5][0] = 4, 4
        assert verify_sudoku_board(board) is False

    def test_duplicate_in_box(self) -> None:
        board = _empty_board()
        board[0][0], board[1][1] = 4, 4
        assert verify_sudoku_board(board) is False


class TestZeroStriping:
    def test_single_zero(self) -> None:
        grid = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
        set_matrix_zeros(grid)
        assert grid == [[1, 0, 1], [0, 0, 0], [1, 0, 1]]

    def test_zero_in_first_row_and_column(self) -> None:
        grid = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]
        set_matrix_zeros(grid)
        assert grid == [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]

    def test_no_zeros_unchanged(self) -> None:
        grid = [[1, 2], [3, 4]]
        set_matrix_zeros(grid)
        assert grid == [[1, 2], [3, 4]]

    def test_all_zeros(self) -> None:
        grid = [[0, 0], [0, 0]]
        set_matrix_zeros(grid)
        assert grid == [[0, 0], [0, 0]]

    def test_empty_matrix_is_noop(self) -> None:
        grid: List[List[int]] = []
        set_matrix_zeros(grid)
        assert grid == []
