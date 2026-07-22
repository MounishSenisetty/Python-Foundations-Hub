"""Tests for the ``foundations.pythonic_oop`` modules."""

from decimal import Decimal

import pytest

from foundations.pythonic_oop.composition_vs_inheritance import (
    AlertService,
    FlakyChannel,
    InMemoryChannel,
    RetryingChannel,
)
from foundations.pythonic_oop.dunder_collections import Bookshelf
from foundations.pythonic_oop.properties_and_validation import (
    BankAccount,
    Thermostat,
)


class TestThermostat:
    def test_valid_temperature_round_trip(self) -> None:
        assert Thermostat(21.5).celsius == 21.5

    def test_fahrenheit_is_derived(self) -> None:
        assert Thermostat(20.0).fahrenheit == 68.0

    def test_setter_revalidates_after_construction(self) -> None:
        unit = Thermostat(20.0)
        unit.celsius = 25.0
        assert unit.fahrenheit == 77.0

    def test_out_of_range_initial_value_rejected(self) -> None:
        with pytest.raises(ValueError):
            Thermostat(-40.0)

    def test_out_of_range_assignment_rejected(self) -> None:
        unit = Thermostat(20.0)
        with pytest.raises(ValueError):
            unit.celsius = 99.0
        assert unit.celsius == 20.0  # failed write left state intact

    def test_non_numeric_assignment_rejected(self) -> None:
        unit = Thermostat(20.0)
        with pytest.raises(TypeError):
            unit.celsius = "hot"  # type: ignore[assignment]

    def test_fahrenheit_is_read_only(self) -> None:
        unit = Thermostat(20.0)
        with pytest.raises(AttributeError):
            unit.fahrenheit = 100.0  # type: ignore[misc]


class TestBankAccount:
    def test_deposit_and_withdraw(self) -> None:
        account = BankAccount("Dana")
        account.deposit(Decimal("100.00"))
        account.withdraw(Decimal("30.00"))
        assert account.balance == Decimal("70.00")

    def test_balance_is_read_only(self) -> None:
        account = BankAccount("Dana")
        with pytest.raises(AttributeError):
            account.balance = Decimal("1000000.00")  # type: ignore[misc]

    def test_non_positive_deposit_rejected(self) -> None:
        account = BankAccount("Dana")
        with pytest.raises(ValueError):
            account.deposit(Decimal("0.00"))

    def test_overdraft_rejected(self) -> None:
        account = BankAccount("Dana")
        account.deposit(Decimal("10.00"))
        with pytest.raises(ValueError):
            account.withdraw(Decimal("10.01"))
        assert account.balance == Decimal("10.00")


class TestBookshelf:
    def test_len_and_bool(self) -> None:
        assert len(Bookshelf(["Dune", "Emma"])) == 2
        assert not Bookshelf()

    def test_integer_indexing(self) -> None:
        assert Bookshelf(["Dune", "Emma"])[1] == "Emma"

    def test_out_of_range_index_raises(self) -> None:
        with pytest.raises(IndexError):
            Bookshelf(["Dune"])[5]

    def test_slicing_returns_a_bookshelf(self) -> None:
        shelf = Bookshelf(["Dune", "Emma", "Ficciones"])
        front = shelf[:2]
        assert isinstance(front, Bookshelf)
        assert front == Bookshelf(["Dune", "Emma"])

    def test_iteration_follows_shelf_order(self) -> None:
        assert list(Bookshelf(["b", "a"])) == ["b", "a"]

    def test_contains_is_case_insensitive(self) -> None:
        shelf = Bookshelf(["Dune"])
        assert "dune" in shelf
        assert "DUNE" in shelf
        assert "Emma" not in shelf

    def test_contains_rejects_non_strings(self) -> None:
        assert 42 not in Bookshelf(["42"])

    def test_equality_and_inequality(self) -> None:
        assert Bookshelf(["a"]) == Bookshelf(["a"])
        assert Bookshelf(["a"]) != Bookshelf(["b"])
        assert Bookshelf(["a"]) != ["a"]  # different type, not equal

    def test_repr_round_trips_through_eval(self) -> None:
        shelf = Bookshelf(["Dune"])
        assert eval(repr(shelf)) == shelf  # noqa: S307 - controlled input

    def test_add_appends_in_order(self) -> None:
        shelf = Bookshelf()
        shelf.add("Dune")
        shelf.add("Emma")
        assert list(shelf) == ["Dune", "Emma"]

    def test_add_rejects_blank_titles(self) -> None:
        shelf = Bookshelf()
        with pytest.raises(ValueError):
            shelf.add("   ")


class TestCompositionOverInheritance:
    def test_alert_service_delivers_via_injected_channel(self) -> None:
        channel = InMemoryChannel()
        AlertService(channel).alert("ops", "disk at 91%")
        assert channel.delivered == [("ops", "disk at 91%")]

    def test_alert_service_rejects_empty_message(self) -> None:
        channel = InMemoryChannel()
        with pytest.raises(ValueError):
            AlertService(channel).alert("ops", "")
        assert channel.delivered == []

    def test_observer_callback_fires_after_send(self) -> None:
        events = []
        service = AlertService(
            InMemoryChannel(), on_sent=lambda who, msg: events.append((who, msg))
        )
        service.alert("ops", "hi")
        assert events == [("ops", "hi")]

    def test_retrying_channel_recovers_from_transient_failures(self) -> None:
        flaky = FlakyChannel(failures_before_success=2)
        RetryingChannel(flaky, attempts=3).send("ops", "hello")
        assert flaky.delivered == [("ops", "hello")]

    def test_retrying_channel_gives_up_when_attempts_exhausted(self) -> None:
        flaky = FlakyChannel(failures_before_success=5)
        with pytest.raises(ConnectionError):
            RetryingChannel(flaky, attempts=3).send("ops", "hello")
        assert flaky.delivered == []

    def test_retrying_channel_rejects_zero_attempts(self) -> None:
        with pytest.raises(ValueError):
            RetryingChannel(InMemoryChannel(), attempts=0)

    def test_behaviours_compose_at_runtime(self) -> None:
        # retry + observer + channel snapped together without subclassing
        events = []
        flaky = FlakyChannel(failures_before_success=1)
        service = AlertService(
            RetryingChannel(flaky, attempts=2),
            on_sent=lambda who, _msg: events.append(who),
        )
        service.alert("ops", "all good")
        assert flaky.delivered == [("ops", "all good")]
        assert events == ["ops"]
