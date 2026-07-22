"""Tests for the ``foundations.pythonic_idioms`` modules."""

import os

import pytest

from foundations.pythonic_idioms.context_managers import (
    Stopwatch,
    rollback_on_error,
    temporary_env_var,
)
from foundations.pythonic_idioms.dictionary_traversal import (
    count_occurrences,
    get_setting,
    group_by_first_letter,
    invert_mapping,
    tally_pairs,
)
from foundations.pythonic_idioms.string_building import (
    build_csv_row,
    concat_lines_slow,
    format_report,
    join_lines,
)


class TestDictionaryTraversal:
    def test_get_setting_returns_stored_value(self) -> None:
        assert get_setting({"mode": "fast"}, "mode") == "fast"

    def test_get_setting_falls_back_to_default(self) -> None:
        assert get_setting({}, "mode", "safe") == "safe"

    def test_count_occurrences(self) -> None:
        assert count_occurrences("aabbbc") == {"a": 2, "b": 3, "c": 1}

    def test_count_occurrences_empty_input(self) -> None:
        assert count_occurrences([]) == {}

    def test_group_by_first_letter_is_case_insensitive(self) -> None:
        grouped = group_by_first_letter(["Apple", "avocado", "Banana"])
        assert grouped == {"a": ["Apple", "avocado"], "b": ["Banana"]}

    def test_group_by_first_letter_rejects_empty_word(self) -> None:
        with pytest.raises(ValueError):
            group_by_first_letter(["ok", ""])

    def test_tally_pairs_sums_per_key(self) -> None:
        assert tally_pairs([("a", 1), ("b", 2), ("a", 3)]) == {"a": 4, "b": 2}

    def test_tally_pairs_returns_plain_dict(self) -> None:
        result = tally_pairs([])
        assert type(result) is dict

    def test_invert_mapping_collects_shared_values(self) -> None:
        assert invert_mapping({"a": 1, "b": 2, "c": 1}) == {1: ["a", "c"], 2: ["b"]}


class TestContextManagers:
    def test_stopwatch_records_elapsed_time(self) -> None:
        with Stopwatch() as watch:
            sum(range(1000))
        assert watch.elapsed > 0.0

    def test_stopwatch_does_not_swallow_exceptions(self) -> None:
        with pytest.raises(RuntimeError):
            with Stopwatch() as watch:
                raise RuntimeError("boom")
        assert watch.elapsed >= 0.0

    def test_temporary_env_var_sets_and_restores(self) -> None:
        name = "FOUNDATIONS_TEST_VAR"
        assert name not in os.environ
        with temporary_env_var(name, "on"):
            assert os.environ[name] == "on"
        assert name not in os.environ

    def test_temporary_env_var_restores_previous_value(self) -> None:
        name = "FOUNDATIONS_TEST_VAR2"
        os.environ[name] = "before"
        try:
            with temporary_env_var(name, "during"):
                assert os.environ[name] == "during"
            assert os.environ[name] == "before"
        finally:
            os.environ.pop(name, None)

    def test_temporary_env_var_restores_on_exception(self) -> None:
        name = "FOUNDATIONS_TEST_VAR3"
        with pytest.raises(ValueError):
            with temporary_env_var(name, "on"):
                raise ValueError("boom")
        assert name not in os.environ

    def test_rollback_on_error_keeps_changes_on_success(self) -> None:
        data = [1, 2]
        with rollback_on_error(data) as batch:
            batch.append(3)
        assert data == [1, 2, 3]

    def test_rollback_on_error_restores_on_failure(self) -> None:
        data = [1, 2]
        with pytest.raises(RuntimeError):
            with rollback_on_error(data) as batch:
                batch.append(3)
                batch.clear()
                raise RuntimeError("boom")
        assert data == [1, 2]


class TestStringBuilding:
    def test_join_matches_slow_concatenation(self) -> None:
        lines = ["alpha", "beta", "gamma"]
        assert join_lines(lines) == concat_lines_slow(lines)

    def test_join_lines_empty_iterable(self) -> None:
        assert join_lines([]) == ""
        assert concat_lines_slow([]) == ""

    def test_join_lines_single_item_has_no_separator(self) -> None:
        assert join_lines(["only"]) == "only"

    def test_build_csv_row_converts_non_strings(self) -> None:
        assert build_csv_row(["id", 7, 3.5]) == "id,7,3.5"

    def test_build_csv_row_custom_separator(self) -> None:
        assert build_csv_row([1, 2, 3], separator="|") == "1|2|3"

    def test_format_report_layout(self) -> None:
        report = format_report("Run", {"ok": 2})
        assert report.splitlines() == ["Run", "===", "ok: 2"]
