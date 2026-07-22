"""Tests for the ``patterns.sliding_window`` modules."""

import pytest

from patterns.sliding_window.longest_substring_unique import (
    longest_substring_unique,
)
from patterns.sliding_window.longest_uniform_substring import (
    longest_uniform_substring,
)
from patterns.sliding_window.substring_anagrams import substring_anagrams


class TestSubstringAnagrams:
    def test_typical_case(self) -> None:
        assert substring_anagrams("cbaebabacd", "abc") == 2

    def test_overlapping_anagrams(self) -> None:
        assert substring_anagrams("abab", "ab") == 3

    def test_no_anagrams(self) -> None:
        assert substring_anagrams("abcd", "xyz") == 0

    def test_pattern_longer_than_text(self) -> None:
        assert substring_anagrams("ab", "abc") == 0

    def test_empty_inputs(self) -> None:
        assert substring_anagrams("", "a") == 0
        assert substring_anagrams("abc", "") == 0

    def test_full_string_is_anagram(self) -> None:
        assert substring_anagrams("bca", "abc") == 1


class TestLongestSubstringUnique:
    def test_typical_case(self) -> None:
        assert longest_substring_unique("abcabcbb") == 3

    def test_all_same_character(self) -> None:
        assert longest_substring_unique("bbbbb") == 1

    def test_mixed(self) -> None:
        assert longest_substring_unique("pwwkew") == 3

    def test_empty_string(self) -> None:
        assert longest_substring_unique("") == 0

    def test_all_unique(self) -> None:
        assert longest_substring_unique("abcdef") == 6

    def test_repeat_outside_window(self) -> None:
        assert longest_substring_unique("abba") == 2


class TestLongestUniformSubstring:
    def test_typical_case(self) -> None:
        assert longest_uniform_substring("AABABBA", 1) == 4

    def test_replace_all_allowed(self) -> None:
        assert longest_uniform_substring("ABBB", 2) == 4

    def test_no_replacements(self) -> None:
        assert longest_uniform_substring("ABAB", 0) == 1

    def test_empty_string(self) -> None:
        assert longest_uniform_substring("", 2) == 0

    def test_single_character(self) -> None:
        assert longest_uniform_substring("A", 5) == 1

    def test_negative_k_raises(self) -> None:
        with pytest.raises(ValueError):
            longest_uniform_substring("AAAB", -1)
