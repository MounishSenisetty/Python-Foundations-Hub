"""Encapsulation with ``@property`` instead of getter/setter methods.

Java-style ``get_x()``/``set_x()`` methods are a smell in Python: they
add ceremony without protection, and they lock callers into a clunky
interface. The Pythonic path is to start with plain public attributes
and introduce ``@property`` only when an attribute actually needs
validation, computation, or read-only behaviour — the calling code
(``account.balance``) never changes.

This module demonstrates all three uses:

* validated read/write properties (``Thermostat.celsius``),
* computed read-only properties (``Thermostat.fahrenheit``),
* invariant-protecting properties (``BankAccount.balance``).

Example:
    >>> Thermostat(20.0).fahrenheit
    68.0
"""

from __future__ import annotations

from decimal import Decimal


class Thermostat:
    """A thermostat with a validated temperature range.

    The stored value lives in the "private by convention" attribute
    ``_celsius``; the public interface is the ``celsius`` property, whose
    setter enforces the supported range on *every* write — including the
    one inside ``__init__``.

    Args:
        celsius: Initial target temperature.

    Raises:
        ValueError: If the initial temperature is out of range.

    Example:
        >>> unit = Thermostat(21.5)
        >>> unit.celsius
        21.5
    """

    MIN_CELSIUS = 5.0
    MAX_CELSIUS = 30.0

    def __init__(self, celsius: float) -> None:
        self.celsius = celsius  # routed through the setter below

    @property
    def celsius(self) -> float:
        """The target temperature in degrees Celsius."""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError("temperature must be a number")
        if not self.MIN_CELSIUS <= value <= self.MAX_CELSIUS:
            raise ValueError(
                f"temperature must be within "
                f"[{self.MIN_CELSIUS}, {self.MAX_CELSIUS}] °C, got {value}"
            )
        self._celsius = float(value)

    @property
    def fahrenheit(self) -> float:
        """The target temperature converted to Fahrenheit.

        Read-only by construction: with no setter defined, assigning to
        ``fahrenheit`` raises ``AttributeError``, so the two scales can
        never disagree.
        """
        return self._celsius * 9 / 5 + 32


class BankAccount:
    """An account whose balance can never be set negative directly.

    ``balance`` is a read-only property; the only mutations are the
    ``deposit`` and ``withdraw`` methods, each of which guards the
    account invariant (``balance >= 0``) before touching state.

    Args:
        owner: Display name of the account holder.

    Example:
        >>> account = BankAccount("Dana")
        >>> account.deposit(Decimal("10.00"))
        >>> account.balance
        Decimal('10.00')
    """

    def __init__(self, owner: str) -> None:
        self.owner = owner
        self._balance = Decimal("0.00")

    @property
    def balance(self) -> Decimal:
        """The current balance. Read-only; use ``deposit``/``withdraw``."""
        return self._balance

    def deposit(self, amount: Decimal) -> None:
        """Add funds to the account.

        Args:
            amount: A positive amount.

        Raises:
            ValueError: If ``amount`` is not strictly positive.
        """
        if amount <= 0:
            raise ValueError("deposit amount must be positive")
        self._balance += amount

    def withdraw(self, amount: Decimal) -> None:
        """Remove funds from the account.

        Args:
            amount: A positive amount no greater than the balance.

        Raises:
            ValueError: If ``amount`` is not strictly positive or exceeds
                the current balance.
        """
        if amount <= 0:
            raise ValueError("withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("insufficient funds")
        self._balance -= amount


if __name__ == "__main__":
    unit = Thermostat(21.0)
    print(f"{unit.celsius} °C == {unit.fahrenheit} °F")

    account = BankAccount("Dana")
    account.deposit(Decimal("125.50"))
    account.withdraw(Decimal("25.50"))
    print(account.owner, "has", account.balance)
