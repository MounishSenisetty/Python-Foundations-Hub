"""Refactoring inheritance hierarchies into injected composition.

Deep hierarchies like ``Notifier -> EmailNotifier ->
RetryingEmailNotifier -> LoggingRetryingEmailNotifier`` multiply: every
new behaviour doubles the number of subclasses, and behaviour is welded
in place at class-definition time.

The composition refactor models each concern as its own small object and
*injects* dependencies through ``__init__``. Behaviours then combine at
runtime — any channel, with or without retry, with any observer — and
each piece is testable in isolation with trivial fakes.

Example:
    >>> channel = InMemoryChannel()
    >>> AlertService(channel).alert("ops", "disk at 91%")
    >>> channel.delivered
    [('ops', 'disk at 91%')]
"""

from __future__ import annotations

from typing import Callable, List, Optional, Protocol, Tuple


class Channel(Protocol):
    """Structural interface for message delivery collaborators.

    Any object with a matching ``send`` method satisfies this protocol —
    no inheritance required. The concrete channels below never mention
    it, yet all conform.
    """

    def send(self, recipient: str, message: str) -> None:
        """Deliver ``message`` to ``recipient``."""
        ...


class InMemoryChannel:
    """A delivery channel that records messages instead of sending them.

    Stands in for real channels (SMTP, SMS, chat webhooks) in examples
    and tests. Any object with a compatible ``send`` method can be
    injected in its place — Python's duck typing needs no shared base
    class.

    Attributes:
        delivered: Every ``(recipient, message)`` pair sent, in order.
    """

    def __init__(self) -> None:
        self.delivered: List[Tuple[str, str]] = []

    def send(self, recipient: str, message: str) -> None:
        """Record a message as delivered.

        Args:
            recipient: Address or identifier of the receiver.
            message: The message body.
        """
        self.delivered.append((recipient, message))


class FlakyChannel:
    """A channel that fails a fixed number of times before succeeding.

    Exists to exercise ``RetryingChannel`` deterministically.

    Args:
        failures_before_success: How many initial ``send`` calls raise.
    """

    def __init__(self, failures_before_success: int) -> None:
        self._remaining_failures = failures_before_success
        self.delivered: List[Tuple[str, str]] = []

    def send(self, recipient: str, message: str) -> None:
        """Send, raising ``ConnectionError`` until failures are used up.

        Args:
            recipient: Address or identifier of the receiver.
            message: The message body.

        Raises:
            ConnectionError: While configured failures remain.
        """
        if self._remaining_failures > 0:
            self._remaining_failures -= 1
            raise ConnectionError("temporary outage")
        self.delivered.append((recipient, message))


class RetryingChannel:
    """Add retry behaviour to *any* channel by wrapping it.

    Under inheritance this would be a ``RetryingXxxChannel`` subclass per
    channel type; as a wrapper it is written once and composes with all
    of them.

    Args:
        inner: The channel to delegate to.
        attempts: Total tries per message; must be at least 1.

    Raises:
        ValueError: If ``attempts`` is less than 1.
    """

    def __init__(self, inner: Channel, attempts: int = 3) -> None:
        if attempts < 1:
            raise ValueError("attempts must be at least 1")
        self._inner = inner
        self._attempts = attempts

    def send(self, recipient: str, message: str) -> None:
        """Delegate to the wrapped channel, retrying on ``ConnectionError``.

        Args:
            recipient: Address or identifier of the receiver.
            message: The message body.

        Raises:
            ConnectionError: If every attempt fails.
        """
        last_error: Optional[ConnectionError] = None
        for _ in range(self._attempts):
            try:
                self._inner.send(recipient, message)
                return
            except ConnectionError as error:
                last_error = error
        assert last_error is not None
        raise last_error


class AlertService:
    """High-level alerting built purely from injected collaborators.

    The service never names a concrete channel class, so swapping email
    for SMS — or a recording fake in tests — requires no change here.

    Args:
        channel: Anything with ``send(recipient, message)``.
        on_sent: Optional callback invoked after each successful send;
            a lightweight observer hook.
    """

    def __init__(
        self,
        channel: Channel,
        on_sent: Optional[Callable[[str, str], None]] = None,
    ) -> None:
        self._channel = channel
        self._on_sent = on_sent

    def alert(self, recipient: str, message: str) -> None:
        """Deliver an alert through the configured channel.

        Args:
            recipient: Address or identifier of the receiver.
            message: The alert text; must be non-empty.

        Raises:
            ValueError: If ``message`` is empty.
        """
        if not message:
            raise ValueError("alert message must not be empty")
        self._channel.send(recipient, message)
        if self._on_sent is not None:
            self._on_sent(recipient, message)


if __name__ == "__main__":
    log: List[str] = []
    flaky = FlakyChannel(failures_before_success=2)
    service = AlertService(
        RetryingChannel(flaky, attempts=3),
        on_sent=lambda recipient, _msg: log.append(f"notified {recipient}"),
    )
    service.alert("ops@example.com", "disk usage at 91%")
    print(flaky.delivered, log)
