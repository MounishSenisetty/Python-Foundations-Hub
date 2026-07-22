"""Tests for the ``foundations.code_smells_and_gotchas`` modules."""

from decimal import Decimal

import pytest

from foundations.code_smells_and_gotchas.float_precision import (
    add_money,
    floats_are_close,
    naive_float_equal,
    round_to_cents,
    split_bill,
    to_money,
)
from foundations.code_smells_and_gotchas.mutable_defaults import (
    append_to,
    append_to_shared,
    report_value,
)
from foundations.code_smells_and_gotchas.shadow_variables import (
    deduplicate,
    merge_mappings,
    normalize_text,
    partition_by_type,
)


class TestMutableDefaults:
    def test_shared_default_leaks_state_between_calls(self) -> None:
        first = append_to_shared(1)
        second = append_to_shared(2)
        assert first is second  # the very same list object
        assert 1 in second and 2 in second

    def test_sentinel_fix_isolates_calls(self) -> None:
        assert append_to(1) == [1]
        assert append_to(2) == [2]  # no state carried over

    def test_sentinel_fix_still_accepts_explicit_bucket(self) -> None:
        bucket = [0]
        assert append_to(1, bucket) == [0, 1]
        assert bucket == [0, 1]

    def test_report_value_distinguishes_omitted_from_none(self) -> None:
        assert report_value() == "no value provided"
        assert report_value(None) == "received None"
        assert report_value(3) == "received 3"


class TestFloatPrecision:
    def test_binary_float_equality_fails(self) -> None:
        assert naive_float_equal(0.1 + 0.2, 0.3) is False

    def test_isclose_comparison_succeeds(self) -> None:
        assert floats_are_close(0.1 + 0.2, 0.3) is True

    def test_abs_tol_handles_near_zero(self) -> None:
        assert floats_are_close(1e-12, 0.0, abs_tol=1e-9) is True

    def test_decimal_addition_is_exact(self) -> None:
        assert add_money("0.10", "0.20") == Decimal("0.30")

    def test_to_money_rejects_floats(self) -> None:
        with pytest.raises(TypeError):
            to_money(0.1)

    def test_round_to_cents_half_up(self) -> None:
        assert round_to_cents("2.675") == Decimal("2.68")
        assert round_to_cents("2.674") == Decimal("2.67")

    def test_split_bill_shares_sum_exactly(self) -> None:
        shares = split_bill("100.00", 3)
        assert sum(shares) == Decimal("100.00")
        assert len(shares) == 3

    def test_split_bill_rejects_non_positive_ways(self) -> None:
        with pytest.raises(ValueError):
            split_bill("10.00", 0)
        with pytest.raises(ValueError):
            split_bill("10.00", -2)


class TestShadowVariables:
    def test_deduplicate_preserves_first_seen_order(self) -> None:
        assert deduplicate([3, 1, 3, 2, 1]) == [3, 1, 2]

    def test_deduplicate_empty_input(self) -> None:
        assert deduplicate([]) == []

    def test_merge_mappings_overrides_win(self) -> None:
        merged = merge_mappings({"a": 1, "b": 2}, {"b": 9})
        assert merged == {"a": 1, "b": 9}

    def test_merge_mappings_leaves_inputs_untouched(self) -> None:
        base = {"a": 1}
        overrides = {"b": 2}
        merge_mappings(base, overrides)
        assert base == {"a": 1} and overrides == {"b": 2}

    def test_normalize_text_collapses_whitespace(self) -> None:
        assert normalize_text("  too   many\tspaces \n") == "too many spaces"

    def test_partition_by_type(self) -> None:
        matching, rest = partition_by_type([1, "a", 2.0, "b"], str)
        assert matching == ["a", "b"]
        assert rest == [1, 2.0]

    def test_builtins_still_callable_after_import(self) -> None:
        # The whole point of the refactor: list/dict/str/type stay usable.
        assert list("ab") == ["a", "b"]
        assert dict(a=1) == {"a": 1}
        assert str(7) == "7"
        assert type("x") is str
