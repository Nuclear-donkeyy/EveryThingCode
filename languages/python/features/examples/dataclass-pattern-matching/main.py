from __future__ import annotations

import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Login:
    user: str
    success: bool
    ip: str


@dataclass(frozen=True)
class Purchase:
    user: str
    amount: float
    currency: str


@dataclass(frozen=True)
class PasswordReset:
    user: str
    requested_by_admin: bool


def describe_event(event: object) -> str:
    if sys.version_info >= (3, 10):
        return describe_event_with_match(event)
    return describe_event_without_match(event)


def describe_event_with_match(event: object) -> str:
    source = """
def _describe(event):
    match event:
        case Login(user=user, success=False, ip=ip):
            return f"review failed login for {user} from {ip}"
        case Login(user=user, success=True):
            return f"record successful login for {user}"
        case Purchase(user=user, amount=amount, currency="USD") if amount >= 100:
            return f"send high-value USD receipt to {user}: {amount:.2f}"
        case Purchase(user=user, amount=amount, currency=currency):
            return f"record purchase for {user}: {amount:.2f} {currency}"
        case PasswordReset(user=user, requested_by_admin=True):
            return f"admin-triggered reset for {user}"
        case PasswordReset(user=user):
            return f"user-triggered reset for {user}"
        case _:
            return "ignore unknown event"
"""
    namespace = {
        "Login": Login,
        "PasswordReset": PasswordReset,
        "Purchase": Purchase,
    }
    exec(source, namespace)
    return namespace["_describe"](event)


def describe_event_without_match(event: object) -> str:
    if isinstance(event, Login):
        if not event.success:
            return f"review failed login for {event.user} from {event.ip}"
        return f"record successful login for {event.user}"

    if isinstance(event, Purchase):
        if event.currency == "USD" and event.amount >= 100:
            return f"send high-value USD receipt to {event.user}: {event.amount:.2f}"
        return f"record purchase for {event.user}: {event.amount:.2f} {event.currency}"

    if isinstance(event, PasswordReset):
        if event.requested_by_admin:
            return f"admin-triggered reset for {event.user}"
        return f"user-triggered reset for {event.user}"

    return "ignore unknown event"


def main() -> None:
    events = [
        Login(user="ada", success=True, ip="10.0.0.4"),
        Login(user="linus", success=False, ip="10.0.0.9"),
        Purchase(user="grace", amount=149.0, currency="USD"),
        PasswordReset(user="ada", requested_by_admin=False),
    ]

    mode = "match/case" if sys.version_info >= (3, 10) else "compatible if/else"
    print(f"python={sys.version.split()[0]} mode={mode}")
    for event in events:
        print(f"- {describe_event(event)}")


if __name__ == "__main__":
    main()
