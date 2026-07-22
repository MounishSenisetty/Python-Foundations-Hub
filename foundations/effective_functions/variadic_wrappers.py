"""Variadic arguments, transparent forwarding, and decorators.

``*args`` and ``**kwargs`` let a function accept — and, crucially,
*forward* — arbitrary arguments. That forwarding is the mechanism behind
every well-behaved wrapper and decorator: the wrapper takes
``(*args, **kwargs)`` and passes them through unchanged, so the wrapped
function's signature never needs to be duplicated.

``functools.wraps`` completes the pattern by copying the wrapped
function's ``__name__``, ``__doc__``, and other metadata onto the
wrapper, keeping introspection and documentation tools honest.

Example:
    >>> product(2, 3, 4)
    24
"""

from __future__ import annotations

import functools
from typing import Any, Callable, Dict, List, Tuple, TypeVar

R = TypeVar("R")


def product(*factors: int) -> int:
    """Multiply any number of integers.

    Args:
        *factors: Zero or more integers.

    Returns:
        The product of all factors; ``1`` when called with none (the
        multiplicative identity, mirroring ``sum()``'s ``0``).
    """
    result = 1
    for factor in factors:
        result *= factor
    return result


def build_tag(name: str, **attributes: str) -> str:
    """Render an HTML-style opening tag from keyword arguments.

    Shows ``**kwargs`` collecting arbitrary keyword arguments into a
    dict, in declaration order.

    Args:
        name: The tag name, e.g. ``"img"``.
        **attributes: Attribute names mapped to their values.

    Returns:
        The rendered tag, e.g. ``<img src="cat.png">``.
    """
    rendered = "".join(f' {key}="{value}"' for key, value in attributes.items())
    return f"<{name}{rendered}>"


def call_with_retries(
    func: Callable[..., R], *args: Any, retries: int = 2, **kwargs: Any
) -> R:
    """Call ``func`` with the given arguments, retrying on exceptions.

    A forwarder: whatever positional and keyword arguments the caller
    supplies (besides ``retries``, claimed by keyword) flow through to
    ``func`` untouched.

    Args:
        func: The callable to invoke.
        *args: Positional arguments forwarded to ``func``.
        retries: Extra attempts after the first failure; must be >= 0.
        **kwargs: Keyword arguments forwarded to ``func``.

    Returns:
        Whatever ``func`` returns on its first successful call.

    Raises:
        ValueError: If ``retries`` is negative.
        Exception: The last exception raised by ``func`` once all
            attempts are exhausted.
    """
    if retries < 0:
        raise ValueError("retries must be non-negative")
    last_error: BaseException
    for _ in range(retries + 1):
        try:
            return func(*args, **kwargs)
        except Exception as error:  # noqa: BLE001 - re-raised after retries
            last_error = error
    raise last_error


def record_calls(
    func: Callable[..., R],
) -> Tuple[Callable[..., R], List[Tuple[Tuple[Any, ...], Dict[str, Any]]]]:
    """Wrap ``func`` so every call's arguments are recorded.

    The decorator pattern in its plainest form: the wrapper forwards
    ``*args``/``**kwargs``, adds one behaviour (recording), and
    ``functools.wraps`` preserves the original function's identity.

    Args:
        func: The callable to observe.

    Returns:
        A ``(wrapper, calls)`` pair. ``calls`` is a live list that gains
        one ``(args, kwargs)`` tuple per invocation of ``wrapper``.
    """
    calls: List[Tuple[Tuple[Any, ...], Dict[str, Any]]] = []

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> R:
        calls.append((args, dict(kwargs)))
        return func(*args, **kwargs)

    return wrapper, calls


def memoize(func: Callable[..., R]) -> Callable[..., R]:
    """Cache results of a pure function by its positional arguments.

    A classic ``@decorator``. Only hashable positional arguments are
    supported, which keeps the cache key trivial; the standard library's
    ``functools.lru_cache`` is the production-grade version.

    Args:
        func: A pure function of hashable positional arguments.

    Returns:
        A wrapped function that computes each distinct input once.
    """
    cache: Dict[Tuple[Any, ...], R] = {}

    @functools.wraps(func)
    def wrapper(*args: Any) -> R:
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrapper


if __name__ == "__main__":
    print(product(2, 3, 4))
    print(build_tag("img", src="cat.png", alt="a cat"))

    @memoize
    def slow_square(n: int) -> int:
        return n * n

    print(slow_square(12), slow_square(12))
