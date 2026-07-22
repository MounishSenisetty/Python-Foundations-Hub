"""Tests for the ``foundations.performance_profiling`` modules."""

import pytest

from foundations.performance_profiling.benchmarking_timeit import (
    BenchmarkResult,
    benchmark,
    compare,
    format_comparison,
)
from foundations.performance_profiling.memory_and_complexity import (
    RegularPoint,
    SlottedPoint,
    instance_footprint,
    running_mean,
    squares_list,
    squares_up_to,
)


class TestBenchmarkingTimeit:
    def test_benchmark_returns_positive_timing(self) -> None:
        result = benchmark(lambda: sum(range(50)), number=10, repeat=2)
        assert isinstance(result, BenchmarkResult)
        assert result.seconds > 0.0

    def test_benchmark_uses_function_name_as_default_label(self) -> None:
        def workload() -> int:
            return 1 + 1

        assert benchmark(workload, number=1, repeat=1).label == "workload"

    def test_per_call_seconds_scales_by_number(self) -> None:
        result = BenchmarkResult(label="x", number=100, seconds=1.0)
        assert result.per_call_seconds == pytest.approx(0.01)

    def test_benchmark_rejects_non_positive_parameters(self) -> None:
        with pytest.raises(ValueError):
            benchmark(lambda: None, number=0)
        with pytest.raises(ValueError):
            benchmark(lambda: None, repeat=0)

    def test_compare_orders_fastest_first(self) -> None:
        results = compare(
            {
                "fast": lambda: None,
                "slow": lambda: sum(range(2000)),
            },
            number=50,
            repeat=1,
        )
        assert list(results) == ["fast", "slow"]

    def test_compare_rejects_empty_input(self) -> None:
        with pytest.raises(ValueError):
            compare({})

    def test_format_comparison_mentions_every_contender(self) -> None:
        results = compare(
            {"a": lambda: None, "bb": lambda: None}, number=5, repeat=1
        )
        table = format_comparison(results)
        assert "a" in table and "bb" in table
        assert "1.00x" in table  # the fastest entry is its own baseline


class TestMemoryAndComplexity:
    def test_slotted_point_is_smaller_than_regular(self) -> None:
        regular = instance_footprint(RegularPoint(1.0, 2.0))
        slotted = instance_footprint(SlottedPoint(1.0, 2.0))
        assert slotted < regular

    def test_slotted_point_rejects_new_attributes(self) -> None:
        point = SlottedPoint(1.0, 2.0)
        with pytest.raises(AttributeError):
            point.z = 3.0  # type: ignore[attr-defined]

    def test_regular_point_allows_new_attributes(self) -> None:
        point = RegularPoint(1.0, 2.0)
        point.z = 3.0  # type: ignore[attr-defined]
        assert point.z == 3.0

    def test_generator_and_list_produce_identical_values(self) -> None:
        assert list(squares_up_to(5)) == squares_list(5)

    def test_generator_is_lazy(self) -> None:
        lazy = squares_up_to(10)
        assert next(lazy) == 0  # nothing computed until asked
        assert next(lazy) == 1

    def test_generator_is_single_pass(self) -> None:
        lazy = squares_up_to(2)
        assert list(lazy) == [0, 1, 4]
        assert list(lazy) == []  # exhausted

    def test_squares_reject_negative_limit(self) -> None:
        with pytest.raises(ValueError):
            squares_list(-1)
        with pytest.raises(ValueError):
            list(squares_up_to(-1))

    def test_running_mean_slides_over_samples(self) -> None:
        assert list(running_mean([1, 2, 3, 4, 5, 6], window=3)) == [
            2.0,
            3.0,
            4.0,
            5.0,
        ]

    def test_running_mean_window_equal_to_length(self) -> None:
        assert list(running_mean([2, 4], window=2)) == [3.0]

    def test_running_mean_window_larger_than_input(self) -> None:
        assert list(running_mean([1, 2], window=5)) == []

    def test_running_mean_rejects_non_positive_window(self) -> None:
        with pytest.raises(ValueError):
            list(running_mean([1, 2, 3], window=0))
