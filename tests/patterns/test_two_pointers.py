"""Tests for the ``patterns.two_pointers`` modules."""

from patterns.two_pointers.is_palindrome_valid import is_palindrome_valid
from patterns.two_pointers.largest_container import largest_container
from patterns.two_pointers.pair_sum_sorted import pair_sum_sorted
from patterns.two_pointers.triplet_sum import triplet_sum


class TestPairSumSorted:
    def test_finds_pair(self) -> None:
        assert pair_sum_sorted([1, 2, 4, 7, 11, 15], 15) == (2, 4)

    def test_returns_smallest_left_index(self) -> None:
        # 2 + 4 == 6 uses the earliest valid left pointer.
        assert pair_sum_sorted([2, 3, 4, 5], 6) == (0, 2)

    def test_no_pair_returns_none(self) -> None:
        assert pair_sum_sorted([1, 2, 3], 7) is None

    def test_empty_and_single(self) -> None:
        assert pair_sum_sorted([], 5) is None
        assert pair_sum_sorted([5], 5) is None

    def test_negative_numbers(self) -> None:
        assert pair_sum_sorted([-5, -2, 0, 3, 8], -2) == (0, 3)


class TestTripletSum:
    def test_typical_case(self) -> None:
        assert triplet_sum([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]]

    def test_all_zeros_deduplicated(self) -> None:
        assert triplet_sum([0, 0, 0, 0]) == [[0, 0, 0]]

    def test_no_triplet(self) -> None:
        assert triplet_sum([1, 2, 3]) == []

    def test_fewer_than_three(self) -> None:
        assert triplet_sum([1, -1]) == []
        assert triplet_sum([]) == []

    def test_duplicates_removed(self) -> None:
        result = triplet_sum([-2, 0, 0, 2, 2])
        assert result == [[-2, 0, 2]]


class TestIsPalindromeValid:
    def test_alphanumeric_palindrome(self) -> None:
        assert is_palindrome_valid("A man, a plan, a canal: Panama") is True

    def test_not_a_palindrome(self) -> None:
        assert is_palindrome_valid("race a car") is False

    def test_only_punctuation_is_palindrome(self) -> None:
        assert is_palindrome_valid(" ") is True
        assert is_palindrome_valid(".,") is True

    def test_empty_string(self) -> None:
        assert is_palindrome_valid("") is True

    def test_single_character(self) -> None:
        assert is_palindrome_valid("a") is True

    def test_mixed_case_and_digits(self) -> None:
        assert is_palindrome_valid("0P") is False
        assert is_palindrome_valid("1a2a1") is True


class TestLargestContainer:
    def test_typical_case(self) -> None:
        assert largest_container([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49

    def test_two_lines(self) -> None:
        assert largest_container([1, 1]) == 1

    def test_increasing_heights(self) -> None:
        assert largest_container([1, 2, 3, 4, 5]) == 6

    def test_fewer_than_two(self) -> None:
        assert largest_container([]) == 0
        assert largest_container([5]) == 0
