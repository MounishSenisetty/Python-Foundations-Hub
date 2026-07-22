"""Validate a partially filled 9x9 Sudoku board.

A board is valid when no row, no column, and no 3x3 sub-box contains a repeated
digit among its filled cells. Empty cells impose no constraint. Sets give each
of these "no duplicates" checks in constant time per cell, so the whole board
is validated in a single pass over its 81 cells.

Intuition:
    Maintain one set of seen digits per row, per column, and per box. For each
    filled cell, the box index is derived from ``(row // 3, col // 3)``. If a
    digit is already present in any of its three sets, the board is invalid;
    otherwise record it and continue.

Time complexity: O(1) — the board is a fixed 9x9 (81 cells).
Space complexity: O(1) — at most 9 sets of 9 digits each.
"""

from __future__ import annotations

from typing import List, Set, Tuple


def verify_sudoku_board(board: List[List[int]]) -> bool:
    """Report whether a 9x9 Sudoku board is valid so far.

    Args:
        board: A 9x9 grid of integers where ``0`` marks an empty cell and
            ``1``-``9`` are filled digits.

    Returns:
        ``True`` if no row, column, or 3x3 box contains a duplicate digit,
        otherwise ``False``. A completely empty board is valid.
    """
    rows: List[Set[int]] = [set() for _ in range(9)]
    cols: List[Set[int]] = [set() for _ in range(9)]
    boxes: List[Set[int]] = [set() for _ in range(9)]

    for r in range(9):
        for c in range(9):
            digit = board[r][c]
            if digit == 0:
                continue
            box = (r // 3) * 3 + (c // 3)
            if digit in rows[r] or digit in cols[c] or digit in boxes[box]:
                return False
            rows[r].add(digit)
            cols[c].add(digit)
            boxes[box].add(digit)

    return True


def _empty_board() -> List[List[int]]:
    return [[0] * 9 for _ in range(9)]


if __name__ == "__main__":
    grid: List[List[int]] = _empty_board()
    positions: Tuple[Tuple[int, int, int], ...] = ((0, 0, 5), (0, 1, 3), (1, 0, 6))
    for row, col, val in positions:
        grid[row][col] = val
    print(verify_sudoku_board(grid))  # True

    grid[0][2] = 5  # duplicate 5 in the top-left box
    print(verify_sudoku_board(grid))  # False
