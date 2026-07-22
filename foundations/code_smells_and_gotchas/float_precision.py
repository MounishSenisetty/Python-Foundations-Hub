"""Floating-point pitfalls and exact arithmetic with ``decimal.Decimal``.

Binary floats cannot represent most decimal fractions exactly: ``0.1``
is stored as the nearest base-2 fraction, which is why
``0.1 + 0.2 == 0.3`` is ``False``. That error is harmless for physics
and fatal for invoices.

Rules of thumb implemented here:

* Comparing floats — use a tolerance (``math.isclose``), never ``==``.
* Money — use ``decimal.Decimal`` constructed from *strings* (building a
  ``Decimal`` from a float imports the float's error), and round with
  ``quantize`` and an explicit rounding mode.

Example:
    >>> floats_are_close(0.1 + 0.2, 0.3)
    True
    >>> add_money("0.10", "0.20")
    Decimal('0.30')
"""

from __future__ import annotations

import math
from decimal import ROUND_HALF_UP, Decimal
from typing import List, Union

MoneyInput = Union[str, int, Decimal]

_CENTS = Decimal("0.01")


def naive_float_equal(left: float, right: float) -> bool:
    """Compare floats with ``==`` — kept to demonstrate the failure.

    Args:
        left: First value.
        right: Second value.

    Returns:
        Whether the two floats are *bit-for-bit* equal, which is
        frequently ``False`` for mathematically equal expressions.
    """
    return left == right


def floats_are_close(
    left: float, right: float, *, rel_tol: float = 1e-9, abs_tol: float = 0.0
) -> bool:
    """Compare floats the safe way, within a tolerance.

    Thin wrapper over ``math.isclose`` so the recommended comparison has
    a named, discoverable home in this codebase.

    Args:
        left: First value.
        right: Second value.
        rel_tol: Maximum allowed relative difference.
        abs_tol: Minimum absolute tolerance, useful near zero.

    Returns:
        ``True`` when the values are equal within tolerance.
    """
    return math.isclose(left, right, rel_tol=rel_tol, abs_tol=abs_tol)


def to_money(amount: MoneyInput) -> Decimal:
    """Convert a safe input type into an exact ``Decimal`` amount.

    Floats are rejected deliberately: ``Decimal(0.1)`` preserves the
    binary representation error (``0.1000000000000000055511...``), which
    defeats the purpose of using ``Decimal`` at all.

    Args:
        amount: A string like ``"19.99"``, an int, or an existing
            ``Decimal``.

    Returns:
        The amount as a ``Decimal``.

    Raises:
        TypeError: If ``amount`` is a float.
    """
    if isinstance(amount, float):
        raise TypeError("construct money from str/int/Decimal, not float")
    return Decimal(amount)


def add_money(*amounts: MoneyInput) -> Decimal:
    """Sum monetary amounts exactly.

    Args:
        *amounts: Any number of money values accepted by ``to_money``.

    Returns:
        The exact sum as a ``Decimal``.
    """
    total = Decimal("0")
    for amount in amounts:
        total += to_money(amount)
    return total


def round_to_cents(amount: MoneyInput) -> Decimal:
    """Round a monetary amount to two places, half-up.

    Bankers' rounding (``ROUND_HALF_EVEN``) is the ``Decimal`` default;
    retail pricing usually expects ``ROUND_HALF_UP``, so the mode is
    pinned explicitly.

    Args:
        amount: Money value accepted by ``to_money``.

    Returns:
        The amount quantised to cents.
    """
    return to_money(amount).quantize(_CENTS, rounding=ROUND_HALF_UP)


def split_bill(total: MoneyInput, ways: int) -> List[Decimal]:
    """Split a bill into equal cent-precise shares that sum exactly.

    The naive ``total / ways`` rounds every share the same way and can
    lose or invent cents. Here the remainder is folded into the final
    share so the parts always reconstruct the whole.

    Args:
        total: The amount to split.
        ways: Number of shares; must be positive.

    Returns:
        A list of ``ways`` amounts summing exactly to ``total``.

    Raises:
        ValueError: If ``ways`` is not a positive integer.
    """
    if ways <= 0:
        raise ValueError("ways must be a positive integer")
    exact_total = round_to_cents(total)
    base_share = (exact_total / ways).quantize(_CENTS, rounding=ROUND_HALF_UP)
    shares = [base_share] * (ways - 1)
    shares.append(exact_total - base_share * (ways - 1))
    return shares


if __name__ == "__main__":
    print("0.1 + 0.2 == 0.3 ?", naive_float_equal(0.1 + 0.2, 0.3))
    print("isclose          ?", floats_are_close(0.1 + 0.2, 0.3))
    print("exact sum        :", add_money("0.10", "0.20"))
    print("split 100 by 3   :", split_bill("100.00", 3))
