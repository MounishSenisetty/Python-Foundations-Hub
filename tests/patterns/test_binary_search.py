"""Tests for the ``patterns.binary_search`` modules."""

import pytest

from patterns.binary_search.cutting_wood import cutting_wood
from patterns.binary_search.find_insertion_index import find_insertion_index
from patterns.binary_search.first_last_occurrences import first_last_occurrences
from patterns.binary_search.target_in_rotated_array import search_rotated


class TestFindInsertionIndex:
    def test_target_present(self) -> None:
        assert find_insertion_index([1, 3, 5, 6], 5) == 2

    def test_target_absent_middle(self) -> None:
        assert find_insertion_index([1, 3, 5, 6], 2) == 1

    def test_target_beyond_end(self) -> None:
        assert find_insertion_index([1, 3, 5, 6], 7) == 4

    def test_target_before_start(self) -> None:
        assert find_insertion_index([1, 3, 5, 6], 0) == 0

    def test_empty_array(self) -> None:
        assert find_insertion_index([], 5) == 0

    def test_duplicates_returns_leftmost(self) -> None:
        assert find_insertion_index([1, 2, 2, 2, 3], 2) == 1


class TestFirstLastOccurrences:
    def test_typical_case(self) -> None:
        assert first_last_occurrences([5, 7, 7, 8, 8, 10], 8) == (3, 4)

    def test_absent_target(self) -> None:
        assert first_last_occurrences([5, 7, 7, 8, 8, 10], 6) == (-1, -1)

    def test_single_occurrence(self) -> None:
        assert first_last_occurrences([5, 7, 7, 8, 8, 10], 5) == (0, 0)

    def test_all_same(self) -> None:
        assert first_last_occurrences([2, 2, 2, 2], 2) == (0, 3)

    def test_empty_array(self) -> None:
        assert first_last_occurrences([], 1) == (-1, -1)

    def test_last_element(self) -> None:
        assert first_last_occurrences([1, 2, 3], 3) == (2, 2)


class TestCuttingWood:
    def test_typical_case(self) -> None:
        assert cutting_wood([2, 6, 3, 8], 7) == 3

    def test_quota_too_high(self) -> None:
        assert cutting_wood([1, 2, 3], 100) == 0

    def test_exact_quota(self) -> None:
        # Blade at 4 yields (5-4)+(6-4)=3.
        assert cutting_wood([5, 6], 3) == 4

    def test_zero_quota(self) -> None:
        assert cutting_wood([4, 5, 6], 0) == 6

    def test_negative_quota_raises(self) -> None:
        with pytest.raises(ValueError):
            cutting_wood([1, 2, 3], -1)


class TestSearchRotated:
    def test_target_in_rotated(self) -> None:
        assert search_rotated([4, 5, 6, 7, 0, 1, 2], 0) == 4

    def test_target_absent(self) -> None:
        assert search_rotated([4, 5, 6, 7, 0, 1, 2], 3) == -1

    def test_single_element_found(self) -> None:
        assert search_rotated([1], 1) == 0

    def test_single_element_absent(self) -> None:
        assert search_rotated([1], 2) == -1

    def test_not_rotated(self) -> None:
        assert search_rotated([1, 2, 3, 4, 5], 4) == 3

    def test_empty_array(self) -> None:
        assert search_rotated([], 1) == -1

    def test_pivot_element(self) -> None:
        assert search_rotated([4, 5, 6, 7, 0, 1, 2], 7) == 3
