"""Tests for the ``foundations.effective_functions`` modules."""

import pytest

from foundations.effective_functions.higher_order_pipeline import (
    compose,
    double,
    doubled_positives_comprehension,
    doubled_positives_functional,
    increment,
    pipeline,
)
from foundations.effective_functions.typed_contracts import (
    TypedRegistry,
    apply_twice,
    first_matching,
    map_optional,
)
from foundations.effective_functions.variadic_wrappers import (
    build_tag,
    call_with_retries,
    memoize,
    product,
    record_calls,
)


class TestVariadicWrappers:
    def test_product_of_several_factors(self) -> None:
        assert product(2, 3, 4) == 24

    def test_product_of_nothing_is_identity(self) -> None:
        assert product() == 1

    def test_build_tag_renders_keyword_attributes(self) -> None:
        assert build_tag("img", src="cat.png") == '<img src="cat.png">'

    def test_build_tag_without_attributes(self) -> None:
        assert build_tag("br") == "<br>"

    def test_call_with_retries_forwards_arguments(self) -> None:
        assert call_with_retries(divmod, 7, 3) == (2, 1)

    def test_call_with_retries_recovers_from_failures(self) -> None:
        attempts = []

        def flaky() -> str:
            attempts.append(1)
            if len(attempts) < 3:
                raise ConnectionError("down")
            return "ok"

        assert call_with_retries(flaky, retries=2) == "ok"
        assert len(attempts) == 3

    def test_call_with_retries_reraises_after_exhaustion(self) -> None:
        def always_fails() -> None:
            raise ConnectionError("down")

        with pytest.raises(ConnectionError):
            call_with_retries(always_fails, retries=1)

    def test_call_with_retries_rejects_negative_retries(self) -> None:
        with pytest.raises(ValueError):
            call_with_retries(len, [], retries=-1)

    def test_record_calls_captures_args_and_kwargs(self) -> None:
        wrapped, calls = record_calls(build_tag)
        wrapped("img", src="a.png")
        wrapped("br")
        assert calls == [(("img",), {"src": "a.png"}), (("br",), {})]

    def test_record_calls_preserves_metadata(self) -> None:
        wrapped, _ = record_calls(build_tag)
        assert wrapped.__name__ == "build_tag"
        assert wrapped.__doc__ == build_tag.__doc__

    def test_memoize_computes_each_input_once(self) -> None:
        evaluations = []

        @memoize
        def square(n: int) -> int:
            evaluations.append(n)
            return n * n

        assert square(4) == 16
        assert square(4) == 16
        assert square(5) == 25
        assert evaluations == [4, 5]


class TestHigherOrderPipeline:
    def test_functional_and_comprehension_agree(self) -> None:
        data = [-2, -1, 0, 1, 2, 3]
        assert doubled_positives_functional(data) == [2, 4, 6]
        assert doubled_positives_functional(data) == (
            doubled_positives_comprehension(data)
        )

    def test_empty_input_yields_empty_output(self) -> None:
        assert doubled_positives_functional([]) == []
        assert doubled_positives_comprehension([]) == []

    def test_compose_applies_right_to_left(self) -> None:
        assert compose(double, increment)(10) == 22  # double(increment(10))

    def test_compose_of_nothing_is_identity(self) -> None:
        assert compose()(99) == 99

    def test_pipeline_applies_left_to_right(self) -> None:
        assert pipeline(10, [double, increment]) == 21  # increment(double(10))

    def test_pipeline_with_no_steps_returns_value(self) -> None:
        assert pipeline("unchanged", []) == "unchanged"

    def test_pure_helpers_do_not_mutate_input(self) -> None:
        data = [1, -1]
        doubled_positives_functional(data)
        assert data == [1, -1]


class TestTypedContracts:
    def test_first_matching_finds_first_hit(self) -> None:
        assert first_matching([1, 4, 6], lambda n: n % 2 == 0) == 4

    def test_first_matching_returns_none_when_absent(self) -> None:
        assert first_matching([1, 3, 5], lambda n: n % 2 == 0) is None

    def test_apply_twice(self) -> None:
        assert apply_twice(lambda n: n + 3, 10) == 16

    def test_map_optional_applies_when_present(self) -> None:
        assert map_optional("shout", str.upper) == "SHOUT"

    def test_map_optional_propagates_none(self) -> None:
        assert map_optional(None, str.upper) is None

    def test_registry_round_trip(self) -> None:
        registry: TypedRegistry[int] = TypedRegistry()
        registry.register("answer", 42)
        assert registry.get("answer") == 42
        assert registry.names() == ["answer"]

    def test_registry_get_missing_returns_none(self) -> None:
        registry: TypedRegistry[str] = TypedRegistry()
        assert registry.get("ghost") is None

    def test_registry_rejects_duplicate_names(self) -> None:
        registry: TypedRegistry[int] = TypedRegistry()
        registry.register("answer", 42)
        with pytest.raises(KeyError):
            registry.register("answer", 43)
